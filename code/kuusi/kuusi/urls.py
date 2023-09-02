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

from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.static import static

from web.views import route_index
from web.http import route_add_suggestion

from kuusi.settings import STATIC_URL, STATIC_ROOT

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', route_index, name='route_index'),
    re_path('(?P<language_code>[a-z]+)/(?P<id>d6[a-zA-Z0-9]+)', route_index, name='route_index'),
    re_path('(?P<id>d6[a-zA-Z0-9]+)', route_index, name='route_index'),
    re_path('(?P<language_code>[a-z]+)', route_index, name='route_index'),
    path('api/i18n/add_suggestion', route_add_suggestion, name='route_add_suggestion'),
] + static(STATIC_URL, document_root=STATIC_ROOT,show_indexes=True)