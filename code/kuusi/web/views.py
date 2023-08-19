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
from django.http import HttpRequest, HttpResponse
from django.template import loader
from django.utils.translation import gettext_lazy as _


from web.models import Page


def route_index(request: HttpRequest):
    template = loader.get_template('index.html')
    page_id = request.GET.get("page")
    page = None
    if page_id:
        page = Page.objects.get(pk=page_id)
    else:
        page = Page.objects.first()
        
    context = {
        "page": page
    }
    return HttpResponse(template.render(context, request))

