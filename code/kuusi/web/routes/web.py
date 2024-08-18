"""
kuusi
Copyright (C) 2014-2024  Christoph Müller  <mail@chmr.eu>

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
from django.core.cache import cache
from typing import List, Tuple, Dict
from django.http import (
    HttpResponse,
    HttpResponseNotAllowed,
    HttpResponseRedirect
)
from django.http import Http404
from django.template import loader
from django.utils.translation import gettext_lazy as _
from django.utils import translation
from re import match

from kuusi.settings import (
    KUUSI_NAME,
    ACCELERATION,
    DEBUG,
    LANGUAGE_CODES,
    DEFAULT_LANGUAGE_CODE,
    KUUSI_TRANSLATION_URL
)
from web.models import Page, Session, WebHttpRequest, Category, FacetteSelection, Choosable, ChoosableMeta, FacetteAssignment, Feedback
from web.helper import forward_helper
from web.models.translateable import INCOMPLETE_TRANSLATIONS
from logging import getLogger

logger = getLogger("root")


def get_page_route(page: Page) -> List[Page]: 
    """
    Get a next page and all available pages from the given page as a start point
    """
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
    return pages

def get_session(request: WebHttpRequest, param_id: str=None) -> Tuple[bool, Session]:
    # Get a session object based on the informations present. If no result_id is existing withing the session a new session will be started
    session: Session = None
    is_new = False
    if "result_id" not in request.session:
        session = get_fresh_session(request)
        is_new = True
    else:
        cookie_result_id = request.session.get("result_id")
        if cookie_result_id != param_id:
            session = get_fresh_session(request)
            is_new = True
            logger.debug(f"The id's differed. Creating new session {session.result_id}")
        else:
            session = Session.objects.filter(
                result_id=request.session["result_id"]
            ).first()
            logger.debug(f"Resumed old session {session.result_id}")

    if is_new and param_id is not None: 
        # Load selections of an old session, if needed
        logger.debug(f"Copying selections from {param_id} to {session.result_id}")
        clone_selections(param_id, request, session)
    else:
        logger.debug("Omitting the cloning of selection, as the cookie features the result_id from the query params.")


    request.session["result_id"] = session.result_id
    return is_new, session

def get_fresh_session(request: WebHttpRequest) -> Session:
    user_agent = request.headers.get("user-agent")
    session = Session(user_agent=user_agent)
    session.save()
    session.referrer = request.headers.get("referrer")
    return session

def clone_selections(id: str, request: WebHttpRequest, session: Session):
    old_session = Session.objects.filter(result_id=id).first()
    if session.session_origin is not None and session.session_origin.result_id == id:
        logger.debug(f"Aborting copy to prevent double copy")
        return
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
                user_agent = request.headers.get("user-agent")
                session = Session(user_agent=user_agent, session_origin=old_session)
                session.save()
                request.session["result_id"] = session.result_id
            else:
                logger.debug(
                    f"Skipping selection copy, the session {session} is already linked to session {old_session}"
                )

def get_categories_and_filtered_pages(page: Page, session: Session) -> Tuple[List[Page], List[Category]]: 
    # get the categories in an order fitting the pages
    pages = get_page_route(page)
    # Get Categories and pages suitable for the currently existing session
    cached_version = cache.get(f"get_categories_and_filtered_pages-pages-{session.version}")
    if cached_version:
        logger.debug("Returning cached categories and pages")
        return cache.get(f"get_categories_and_filtered_pages-pages-{session.version}"), cache.get(f"get_categories_and_filtered_pages-categories-{session.version}")
    
    version_comp_pages = []
    chained_page: Page
    for chained_page in pages:
        if chained_page.is_visible(session):
            version_comp_pages.append(chained_page)

    categories = []
    for chained_page in pages:
        # Child categories will be created later, when the steps are created.
        used_in_category = Category.objects.filter(
            target_page=chained_page, child_of__isnull=True
        )
        if used_in_category.count() > 0:
            categories.append(used_in_category.first())
    cache.set(f"get_categories_and_filtered_pages-pages-{session.version}", version_comp_pages)
    cache.set(f"get_categories_and_filtered_pages-categories-{session.version}", categories)
    return version_comp_pages, categories

def build_step_data(categories: List[Category], request: WebHttpRequest):
    step_data = []
    index: int
    category: Category
    for index, category in enumerate(categories):
        minor_steps = []
        category_step = category.to_step(
            request,
            index == categories.__len__() - 1,
        )
        child_categories = Category.objects.filter(child_of=category)
        child_category: Category
        for child_category in child_categories:
            minor_steps.append(
                child_category.to_step(
                    request,
                )
            )
        step = {
            "icon": category.icon,
            "major": category_step,
            "minor": minor_steps,
        }
        step_data.append(step)
    return step_data

def route_outgoing(request: WebHttpRequest, id: int, property: str) -> HttpResponse:
    got = Choosable.objects.filter(pk=id) 
    property = property.upper()
    if got.count() == 1:
        choosable: Choosable = got.first()
        if choosable:
            if property not in choosable.meta:
                raise Http404()
            else:
                choosable.clicked += 1
                choosable.save()
                return HttpResponseRedirect(choosable.meta[property].meta_value)
    raise Http404()


def route_index(request: WebHttpRequest, language_code: str = None, id: str = None):
    # Prevent the route from doing weird stuff with 404-ish routes
    if language_code is not None and language_code not in LANGUAGE_CODES:
        raise Http404()

    # Get the current page
    page_id = request.GET.get("page")
    page = None
    if page_id:
        page = Page.objects.get(catalogue_id=page_id)
    else:
        page = Page.objects.first()

    _, session = get_session(request, id)

    # i18n handling
    request.LANGUAGE_CODE = (
        DEFAULT_LANGUAGE_CODE if not language_code else language_code
    )
    if session.language_code != request.LANGUAGE_CODE:
        logger.debug(f"Session lang was {session.language_code} is now {request.LANGUAGE_CODE}")
        session.language_code = request.LANGUAGE_CODE
        session.save()
    translation.activate(request.LANGUAGE_CODE) 

    # If the id is none -> Redirect the user to a URL representing the entire state
    if id is None or id != session.result_id or language_code is None:
        # DO not redirect on a simple GET request
        # Allowing crawlers to crawl the page for OGP tags
        if request.method != "GET":
            url_suffix = "?page={page.catalogue_id}"
            if "BTN_FORCED_NAVIGATION" in request.POST:
                url_suffix =request.POST["BTN_FORCED_NAVIGATION"]
            return HttpResponseRedirect(f"/{request.LANGUAGE_CODE}/{session.result_id}{url_suffix}")
    # Onboard th session to the request oject 

  
    # TODO: Find a more elegant way to inject these properties into the (Web-)HttpRequest
    request.session_obj = session    
    request.has_errors = False

    # Turbo call handling
    overwrite_status = 200
    base_url = f"/{request.LANGUAGE_CODE}" + ("" if not id else f"/{id}")
    if request.method == "POST":
        overwrite_status, response = forward_helper(
            id, overwrite_status, session, base_url, page, request
        )
        if response and not overwrite_status:
            return response
       

    # Build the navigation/ Categories
    pages, categories = get_categories_and_filtered_pages(page, session)

  
    
    current_location = request.get_full_path()
    # If the user is curently on the start page -> use the first available site as "current location"
    if current_location.__len__() <= 1:
        current_location = base_url + pages[0].href

    """
    In Case the desired page is not active within the current version -> attempt to find the next one suitable

    If not page is suitable, it will result in a 405 later.
    """
    if not page.is_visible(session):
        page = Page.next_visible_page(page, session)

    step_data = build_step_data(categories, request)

    if not page.is_visible(request.session_obj):
        return HttpResponseNotAllowed(_("PAGE_NOT_AVAILABLE"))

    context = {
        "title": KUUSI_NAME,
        "page": page,
        "steps": step_data,
        "acceleration": ACCELERATION,
        "debug": DEBUG,
        "language_codes": LANGUAGE_CODES,
        "language_code": request.LANGUAGE_CODE,
        "session": session,
        "locale_incomplete": language_code in INCOMPLETE_TRANSLATIONS,
        "translation_url": KUUSI_TRANSLATION_URL
    }

    if "accept" in request.headers and "turbo" in request.headers.get("accept"):
        logger.debug(f"This is a turbo call")
    else:
        overwrite_status = 200
        logger.debug(
            f"There is no ext/vnd.turbo-stream.html accept header. Revoking all status code changes."
        )

    logger.debug(f"Status overwrite is {overwrite_status}")
    template = loader.get_template("index.html")

    return HttpResponse(template.render(context, request), status=overwrite_status)


def route_feedback(request: WebHttpRequest,assignment_id: int, choosable_id: int):
    assignment: FacetteAssignment = FacetteAssignment.objects.get(pk=assignment_id)
    choosable: Choosable = Choosable.objects.get(pk=choosable_id)
    session: Session = Session.objects.get(result_id=request.session.get("result_id"))
    is_new = True
    if not assignment.is_flagged(choosable):
        Feedback.objects.create(
            assignment=assignment,
            is_positive=False,
            choosable=choosable
        )
    else:
        is_new = False
        Feedback.objects.filter(assignment=assignment, choosable=choosable).delete()

    url = f"/{session.language_code}/{session.result_id}?page=result-page"
    if is_new:
        url += "&feedback=true"
    url += f"&scroll_to={choosable.pk}"
    return HttpResponseRedirect(url)

