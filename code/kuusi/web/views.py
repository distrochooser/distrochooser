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
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.template import loader
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from kuusi.settings import KUUSI_NAME, ACCELERATION, DEBUG
from web.models import Page, Session, WebHttpRequest, Category, FacetteSelection
from logging import getLogger
logger = getLogger('root')

def route_index(request: WebHttpRequest, id: str = None):
    # TODO: Get the original selections, copy them to the users's own session.
    template = loader.get_template('index.html')
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
            session = Session(
                user_agent = user_agent
            )
            session.save()
            request.session["result_id"] = session.result_id
        else:
            session = Session.objects.filter(result_id=request.session["result_id"]).first()

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
                    if FacetteSelection.objects.filter(session=session, facette=selection.facette).count() == 0:
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
                    session = Session(
                        user_agent = user_agent,
                        session_origin = old_session
                    )
                    session.save()
                    request.session["result_id"] = session.result_id
                else:   
                    logger.debug(f"Skipping selection copy, the session {session} is already linked to session {old_session}")
    
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
        used_in_category = Category.objects.filter(target_page=chained_page,child_of__isnull=True)
        if used_in_category.count() > 0:
            categories.append(used_in_category.first())
    # TODO: These are not properly set within WebHttpRequest class.
    request.has_errors = False
    request.has_warnings = False
    overwrite_status = 200
    if request.method == "POST":  
        stay = False
        if page.can_be_marked and "BTN_MARK_TOGGLE" in request.POST:
            page.toggle_marking(request.session_obj)
            stay = True
            overwrite_status = 422
        result = page.proceed(request)
        if not result:
            if "BTN_NEXT_PAGE_FORCE" in request.POST:
                logger.debug(f"User decided to force to next page even as there are issues present (has_errors={request.has_errors},has_warnings={request.has_warnings})")
                result = True
            else:
                overwrite_status = 422  
        

        if "BTN_FORCED_NAVIGATION" in request.POST:
            value = request.POST.get("BTN_FORCED_NAVIGATION")
            return HttpResponseRedirect(value)
        
        forward_target: Page = None
        attempts  = 0
        if not stay:
            logger.debug(f"The next page is not visible. Starting page skip.")
            # Make sure the user is redirect to a _valid_ page instead of an empty one if the next page is not visible
            forward_target = page.next_page
            while forward_target and not forward_target.is_visible(session):
                if forward_target.next_page.is_visible(session):
                    forward_target = forward_target.next_page
                    logger.debug(f"Forward target is now {forward_target}")
                
                attempts +=1

                if attempts >= 10:
                    break     

            forward_target_href = page.next_page.href if page.next_page else None
            if result:
                if forward_target is not None:
                    forward_target_href = forward_target.href
                return HttpResponseRedirect(forward_target_href)
    current_location = request.get_full_path()
    # If the user is curently on the start page -> use the first available site as "current location"
    if current_location.__len__() <= 1:
        current_location = pages[0].href
    step_data = []
    index: int
    category: Category
    for index, category in enumerate(categories):
        minor_steps = []
        # TODO: Inject language
        category_step = category.to_step(current_location, "en", request.session_obj, index == categories.__len__() - 1)
        child_categories = Category.objects.filter(child_of=category)
        child_category: Category
        for child_category in child_categories: 
            minor_steps.append(
                child_category.to_step(current_location, "en", request.session_obj)
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
        "acceleration":ACCELERATION,
        "debug": DEBUG
    }
    # TODO: create a tree , displaying the behaviours and selection reasons 
    # TODO: Allow the user to display and modify the tree (if allowed)

    if "accept" in request.headers and "turbo" in request.headers.get("accept"):
        logger.debug(f"This is a turbo call")
    else:
        overwrite_status = 200
        logger.debug(f"There is no ext/vnd.turbo-stream.html accept header. Revoking all status code changes.")

    logger.debug(f"Status overwrite is {overwrite_status}")


    return HttpResponse(template.render(context, request), status=overwrite_status)