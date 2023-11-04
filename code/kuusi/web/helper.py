"""
kuusi
Copyright (C) 2014-2023  Christoph Müller <mail@chmr.eu>

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
from typing import Tuple
from django.http import HttpResponse, HttpResponseRedirect
from web.models import Session, Page, WebHttpRequest

from logging import getLogger

logger = getLogger("root")

def forward_helper(id: str, overwrite_status: int, session: Session, base_url: str, page: Page, request: WebHttpRequest) -> Tuple[int, HttpResponse | None]:
    """
    Handles several frontend redirects:

    Language change
    Forced navigation in case of displayed errors

    Returns:
        Tuple [HTTP-Status, Response]
        If the status is none, a response shall be used
        If the status is not none, the status should be used (and the response will be most likely None)
    """
    if "ku-i18n-site-lang-code-change" in request.POST:
        new_code = request.POST.get("ku-i18n-site-lang-code")
        target = f"/{new_code}" + ("" if not id else f"/{id}")
        if request.GET.get("page"):
            target += f"/?page={request.GET.get('page')}"
        return None, HttpResponseRedirect(target)
    stay = False
    if page.can_be_marked and "BTN_MARK_TOGGLE" in request.POST:
        page.toggle_marking(request.session_obj)
        stay = True
        overwrite_status = 422
    result = page.proceed(request)
    if not result:
        if "BTN_NEXT_PAGE_FORCE" in request.POST:
            logger.debug(
                f"User decided to force to next page even as there are issues present (has_errors={request.has_errors},has_warnings={request.has_warnings})"
            )
            result = True
        else:
            overwrite_status = 422

    if "BTN_FORCED_NAVIGATION" in request.POST:
        value = request.POST.get("BTN_FORCED_NAVIGATION")
        return None, HttpResponseRedirect(base_url + value)

    forward_target: Page = None
    attempts = 0
    if not stay:
        logger.debug(f"The next page is not visible. Starting page skip.")
        # Make sure the user is redirect to a _valid_ page instead of an empty one if the next page is not visible
        forward_target = page.next_page
        while forward_target and not forward_target.is_visible(session):
            if forward_target.next_page.is_visible(session):
                forward_target = forward_target.next_page
                logger.debug(f"Forward target is now {forward_target}")

            attempts += 1

            if attempts >= 10:
                break

        forward_target_href = page.next_page.href if page.next_page else None
        if result:
            if forward_target is not None:
                forward_target_href = forward_target.href
            logger.debug(f"Forward target is now {base_url + forward_target_href}")    
            return None, HttpResponseRedirect(base_url + forward_target_href)
    logger.debug(f"The forward helper does not result in any additional responses.")
    return overwrite_status, None