"""
kuusi
Copyright (C) 2014-2025  Christoph Müller  <mail@chmr.eu>

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

from django.http import HttpResponse
from web.models import Session, WebHttpRequest

def route_ack(request: WebHttpRequest, result_id: str):
    session_matches = Session.objects.filter(result_id=result_id)
    if session_matches.count() == 1:
        session = session_matches.first()
        session.is_ack = True
        session.save()
    return HttpResponse("ACK")