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
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.utils.translation import gettext_lazy as _


from web.models import Page, Session, WebHttpRequest
from logging import getLogger
logger = getLogger('root')

def route_index(request: WebHttpRequest):
    template = loader.get_template('index.html')
    page_id = request.GET.get("page")
    page = None
    if page_id:
        page = Page.objects.get(pk=page_id)
    else:
        page = Page.objects.first()
    session = None
    if page.require_session:
        if "result_id" not in request.session:
            user_agent = request.headers.get("user-agent")
            session = Session(
                user_agent = user_agent
            )
            session.save()
            request.session["result_id"] = session.result_id
        else:
            session = Session.objects.filter(result_id=request.session["result_id"]).first()

    # TODO: If the user accesses the site with a GET parameter result_id, create a new session and copy old results.
    request.session_obj = session
    # TODO: These are not properly set within WebHttpRequest class.
    request.has_errors = False
    request.has_warnings = False
    if request.method == "POST":
        result = page.proceed(request)
        if not result:
            if "BTN_NEXT_PAGE_FORCE" in request.POST:
                logger.debug(f"User decided to force to next page even as there are issues present (has_errors={request.has_errors},has_warnings={request.has_warnings})")
                result = True
        if result and page.next_page:
            return HttpResponseRedirect(f"/?page={page.next_page.pk}")
        
    context = {
        "page": page
    }
    return HttpResponse(template.render(context, request))

