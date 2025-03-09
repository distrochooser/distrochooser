"""
distrochooser
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
from logging import getLogger
from django.http import (Http404, HttpResponse)
from django.utils.translation import gettext_lazy as _
from web.models import (Choosable,
                        WebHttpRequest)

logger = getLogger("root")

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
                return HttpResponse()
    raise Http404()


