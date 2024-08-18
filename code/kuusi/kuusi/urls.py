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

from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.static import static

from web.routes.web import route_index, route_outgoing, route_feedback
from web.routes.static import  route_about, route_contact, route_privacy
from web.routes.matrix import route_update
from web.routes.ack import route_ack
from web.routes.data import route_data
from web.routes.bridge import route_distrochooser5_redirect
from web.routes.crawlers import route_robots_txt, route_sitemap_xml

from kuusi.settings import STATIC_URL, STATIC_ROOT

dynamic_routes = [   
    path("update",  route_update, name="route_update"),
    path("robots.txt",  route_robots_txt, name="route_robots_txt"),
    path("sitemap.xml",  route_sitemap_xml, name="sitemap.xml"),
    path("out/<id>/<property>",  route_outgoing, name="route_outgoing"),
    path('', route_index, name='route_index'),
    re_path('(?P<language_code>[a-z]{2,6})/(?P<id>d6[a-zA-Z0-9]+)', route_index, name='route_index'),
    re_path('(?P<language_code>[a-z]{2,6})/(?P<id>d5[a-zA-Z0-9]+)', route_distrochooser5_redirect, name='route_distrochooser5_redirect'),
    re_path('(?P<id>d6[a-zA-Z0-9]+)', route_index, name='route_index'),
    re_path('(?P<language_code>[a-z]{2,6})', route_index, name='route_index')
]

urlpatterns = [
    path("admin", admin.site.urls),
    path("feedback/<assignment_id>/<choosable_id>",  route_feedback, name="route_feedback"),
    re_path('api/ack/(?P<result_id>[a-zA-Z0-9]+)', route_ack),
    re_path("(?P<language_code>[a-z]+)/about", route_about, name="route_about"),
    re_path("(?P<language_code>[a-z]+)/privacy", route_privacy, name="route_privacy"),
    re_path("(?P<language_code>[a-z]+)/contact", route_contact, name="route_contact"),
    re_path("data/(?P<version>[0-9]+)", route_data, name="route_data"),
   
] + static(STATIC_URL, document_root=STATIC_ROOT,show_indexes=True) + dynamic_routes