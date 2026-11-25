"""
distrochooser
Copyright (C) 2014-2026 Christoph Müller <distrochooser@chmr.eu>

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

from logging import getLogger
from django.http import Http404, HttpResponse, JsonResponse
from django.utils.translation import gettext_lazy as _
from web.models import Choosable, WebHttpRequest, Session, Click

logger = getLogger("root")


def route_outgoing(
    request: WebHttpRequest, session_id: int, id: int, property: str
) -> HttpResponse:
    got = Choosable.objects.filter(pk=id)
    sessions = Session.objects.filter(pk=session_id)
    property = property.upper()
    if got.exists() and sessions.exists():
        choosable: Choosable = got.first()
        session: Session = sessions.first()
        if property not in choosable.meta:
            raise Http404()
        else:
            Click(session=session, choosable=choosable).save()
            return HttpResponse()
    raise Http404()


def route_pong(request: WebHttpRequest) -> HttpResponse:
    something = Choosable.objects.all()
    return JsonResponse({"pong": something.count()})
