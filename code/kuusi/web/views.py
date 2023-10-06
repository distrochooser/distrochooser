"""
kuusi
Copyright (C) 2015-2023  Christoph Müller <mail@chmr.eu>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden, HttpResponseNotFound
from django.template import loader
from django.utils.translation import gettext_lazy as _
from django.utils import translation
from django.core.management import call_command
from django.views.decorators.csrf import csrf_exempt
from os.path import join

from kuusi.settings import (
    KUUSI_NAME,
    ACCELERATION,
    DEBUG,
    LANGUAGE_CODES,
    DEFAULT_LANGUAGE_CODE,
    UPDATE_API_KEY, 
    UPDATE_UPLOAD_PATH
)
from web.models import Page, Session, WebHttpRequest, Category, FacetteSelection
from web.helper import forward_helper
from logging import getLogger

logger = getLogger("root")


def route_index(request: WebHttpRequest, language_code: str = None, id: str = None):
    # TODO: Get the original selections, copy them to the users's own session.
    template = loader.get_template("index.html")
    page_id = request.GET.get("page")
    page = None
    if page_id:
        page = Page.objects.get(catalogue_id=page_id)
    else:
        page = Page.objects.first()

    # get the categories in an order fitting the pages
    pages = []
    prev_page = page.previous_page
    while prev_page is not None:
        if prev_page:
            pages = [prev_page] + pages
            prev_page = prev_page.previous_page
        else:
            prev_page = None
    pages.append(page)
    next_page = page.next_page
    while next_page is not None:
        if next_page:
            pages.append(next_page)
            next_page = next_page.next_page
        else:
            next_page = None

    # it is REQUIRED that a possible version selection is done before pages handle with sessions.
    # in best case, there is a welcome page (without cookies) > then the version select -> then the pages following.
    session = None
    if page.require_session:
        # TODO: Make the handling better. TO pick up old results it's required to have a session, but the welcome page should not feature a session due to cookies
        # TODO: Also, get rid of the csrftoken cookie until user gave consent
        if "result_id" not in request.session:
            user_agent = request.headers.get("user-agent")
            session = Session(user_agent=user_agent)
            session.save()
            request.session["result_id"] = session.result_id
        else:
            session = Session.objects.filter(
                result_id=request.session["result_id"]
            ).first()

    # Load selections of an old session
    # TODO: Load correct version!
    if id is not None and session:
        old_session = Session.objects.filter(result_id=id).first()
        if old_session:
            logger.debug(f"Found old session {old_session}")
            if not session.session_origin:
                selections = FacetteSelection.objects.filter(session=old_session)
                selection: FacetteSelection
                for selection in selections:
                    # prevent double copies
                    if (
                        FacetteSelection.objects.filter(
                            session=session, facette=selection.facette
                        ).count()
                        == 0
                    ):
                        selection.pk = None
                        selection.session = session
                        selection.save()
                session.session_origin = old_session
                session.save()
            else:
                if session.session_origin != old_session:
                    logger.debug(f"This is a new session, but the user has a session.")
                    # TODO: Create a new session in case the user clicks on another session link.
                    # TODO: Get rid of redundancy with  above
                    user_agent = request.headers.get("user-agent")
                    session = Session(user_agent=user_agent, session_origin=old_session)
                    session.save()
                    request.session["result_id"] = session.result_id
                else:
                    logger.debug(
                        f"Skipping selection copy, the session {session} is already linked to session {old_session}"
                    )

    # TODO: If the user accesses the site with a GET parameter result_id, create a new session and copy old results.
    # TODO: Prevent that categories are disappearing due to missing session on the first page
    request.session_obj = session
    # Only include the pages fitting the selected version
    version_comp_pages = []
    chained_page: Page
    for chained_page in pages:
        if chained_page.is_visible(session):
            version_comp_pages.append(chained_page)

    pages = version_comp_pages
    categories = []
    for chained_page in pages:
        # Child categories will be created later, when the steps are created.
        used_in_category = Category.objects.filter(
            target_page=chained_page, child_of__isnull=True
        )
        if used_in_category.count() > 0:
            categories.append(used_in_category.first())
    # TODO: These are not properly set within WebHttpRequest class.
    request.has_errors = False
    request.has_warnings = False
    # TODO: Investigate correct approach
    request.LANGUAGE_CODE = DEFAULT_LANGUAGE_CODE if not language_code else language_code
    translation.activate(request.LANGUAGE_CODE)
    overwrite_status = 200
    base_url = f"/{request.LANGUAGE_CODE}" + ("" if not id else f"/{id}")
    if request.method == "POST":
        overwrite_status, response = forward_helper(id, overwrite_status, session, base_url, page, request)
        if response and not overwrite_status:
            return response
    current_location = request.get_full_path()
    # If the user is curently on the start page -> use the first available site as "current location"
    if current_location.__len__() <= 1:
        current_location = base_url  + pages[0].href
    step_data = []

    """
    In Case the desired page is not active within the current version -> attempt to find the next one suitable

    If not page is suitable, it will result in a 405 later.
    """
    if not page.is_visible(session):
        fallback_page = None
        next_page = page.next_page

        next_page: Page
        while next_page is not None:
            if next_page.is_visible(session):
                fallback_page = next_page
                break
            next_page = next_page.next_page
        if fallback_page:
            page = fallback_page

    index: int
    category: Category
    for index, category in enumerate(categories):
        minor_steps = []
        category_step = category.to_step(
            current_location,
            request.LANGUAGE_CODE,
            request.session_obj,
            index == categories.__len__() - 1,
        )
        child_categories = Category.objects.filter(child_of=category)
        child_category: Category
        for child_category in child_categories:
            minor_steps.append(
                child_category.to_step(current_location, request.LANGUAGE_CODE, request.session_obj)
            )
        step = {
            "icon": category.icon,
            "major": category_step,
            "minor": minor_steps,
        }
        step_data.append(step)
    if not page.is_visible(request.session_obj):
        return HttpResponseNotAllowed(_("PAGE_NOT_AVAILABLE"))
    context = {
        "title": KUUSI_NAME,
        "page": page,
        "steps": step_data,
        "acceleration": ACCELERATION,
        "debug": DEBUG,
        "language_codes": LANGUAGE_CODES,
        "language_code": request.LANGUAGE_CODE
    }
    # TODO: create a tree , displaying the behaviours and selection reasons
    # TODO: Allow the user to display and modify the tree (if allowed)

    if "accept" in request.headers and "turbo" in request.headers.get("accept"):
        logger.debug(f"This is a turbo call")
    else:
        overwrite_status = 200
        logger.debug(
            f"There is no ext/vnd.turbo-stream.html accept header. Revoking all status code changes."
        )

    logger.debug(f"Status overwrite is {overwrite_status}")

    return HttpResponse(template.render(context, request), status=overwrite_status)


@csrf_exempt
def route_update(request: WebHttpRequest) -> HttpResponse:
    """
    Update the matrix OTA. Has the same logic as manage.py parse <filename>

    The endpoint receives a set of files, which have their original filenames.
    The first file is considered as "main" file and will be used to trigger the parse mechanism.

    The endpoint requires an Authorization header to feature the value from UPDATE_API_KEY and the method must be POST.
    
    """
    if request.method != "POST":
        return HttpResponseNotAllowed("Not allowed")
    
    header = request.headers.get("Authorization")

    if not header or header != UPDATE_API_KEY:
        return HttpResponseForbidden("Forbidden")
    
    if request.FILES.__len__ == 0:
        return HttpResponseNotFound("File is missing")
    first_file_name = None
    for key, file_content in request.FILES.items():
        if not first_file_name:
            first_file_name = key
        with open(join(UPDATE_UPLOAD_PATH, key), "wb") as file:
            for chunk in file_content.chunks():
                file.write(chunk)
    call_command('parse', join(UPDATE_UPLOAD_PATH, first_file_name))
    return HttpResponse("ok")