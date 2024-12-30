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
from django.urls import path, re_path, include
from django.conf.urls.static import static

from web.routes.web import route_index, route_outgoing, route_feedback
from web.routes.static import  route_about, route_contact, route_privacy, route_support
from web.routes.ack import route_ack
from web.routes.data import route_data
from web.routes.bridge import route_distrochooser5_redirect
from web.routes.crawlers import route_robots_txt, route_sitemap_xml

from rest_framework_nested import routers
from web.rest.choosable import ChoosableViewSet
from web.rest.facette import FacetteViewSet
from web.rest.page import PageViewSet
from web.rest.session import SessionViewSet
from web.rest.category import CategoryViewSet
from web.rest.facetteselection import FacetteSelectionViewSet
from web.rest.facettebehaviour import FacetteBehaviourViewSet
from web.rest.facette import FeedbackViewSet
from web.rest.widget import WidgetViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from kuusi.settings import STATIC_URL, STATIC_ROOT


router = routers.SimpleRouter()
router.register(r'session', SessionViewSet)


router_sessions = routers.NestedDefaultRouter(router, r'session', lookup='session')
router_sessions.register(r'page', PageViewSet, basename='session-pages')

router_page = routers.NestedDefaultRouter(router_sessions, r"page", lookup="page")
router_page.register(r"widget", WidgetViewSet, basename="widget-page")


router_sessions.register(r'facette', FacetteViewSet, basename='session-facettes')
router_sessions.register(r'category', CategoryViewSet, basename='session-categories')
router_sessions.register(r'facetteselection', FacetteSelectionViewSet, basename='session-selections')
router_sessions.register(r'facettebehaviour', FacetteBehaviourViewSet, basename='session-behaviour')
router_sessions.register(r'choosable', ChoosableViewSet, basename='session-choosables')
router_sessions.register(r'feedback', FeedbackViewSet, basename='session-feedback')


urlpatterns = [
    path('rest/', include(router.urls)),
    path('rest/', include(router_sessions.urls)),
    path('rest/', include(router_page.urls)),
    path('rest/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('rest/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path("robots.txt",  route_robots_txt, name="route_robots_txt"),
    path("sitemap.xml",  route_sitemap_xml, name="sitemap.xml"),
    path("out/<id>/<property>",  route_outgoing, name="route_outgoing"),
    path("admin", admin.site.urls)
   
] + static(STATIC_URL, document_root=STATIC_ROOT,show_indexes=True) 