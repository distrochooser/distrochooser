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

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_spectacular.views import (SpectacularAPIView,
                                   SpectacularSwaggerView)
from kuusi.settings import ENABLE_PROFILING, STATIC_ROOT, STATIC_URL, DEBUG
from rest_framework_nested import routers
from web.rest.category import CategoryViewSet
from web.rest.choosable import ChoosableViewSet
from web.rest.facette import (AssignmentFeedbackViewSet, FacetteViewSet,
                              FeedbackViewSet)
from web.rest.facettebehaviour import FacetteBehaviourViewSet
from web.rest.facetteselection import FacetteSelectionViewSet
from web.rest.language import LanguageFeedbackViewSet
from web.rest.languagevote import LanguageFeedbackVoteViewset
from web.rest.metafilter import MetaFilterValueViewSet
from web.rest.page import PageMarkingViewSet, PageViewSet
from web.rest.session import MetaTagViewset, SessionViewSet
from web.rest.widget import WidgetViewSet
from web.routes.data import route_data
from web.routes.web import route_outgoing

router = routers.SimpleRouter()
router.register(r'session', SessionViewSet)
router.register(r'metatags', MetaTagViewset, basename="metatags")


router_sessions = routers.NestedDefaultRouter(router, r'session', lookup='session')
router_sessions.register(r'page', PageViewSet, basename='session-pages')

router_page = routers.NestedDefaultRouter(router_sessions, r"page", lookup="page")
router_page.register(r"widget", WidgetViewSet, basename="widget-page")

router_page.register(r"marking", PageMarkingViewSet, basename="marking-page")


router_sessions.register(r'facette', FacetteViewSet, basename='session-facettes')
router_sessions.register(r'category', CategoryViewSet, basename='session-categories')
router_sessions.register(r'facetteselection', FacetteSelectionViewSet, basename='session-selections')
router_sessions.register(r'facettebehaviour', FacetteBehaviourViewSet, basename='session-behaviour')
router_sessions.register(r'choosable', ChoosableViewSet, basename='session-choosables')
router_sessions.register(r'feedback', FeedbackViewSet, basename='session-feedback')
router_sessions.register(r'assignmentfeedback', AssignmentFeedbackViewSet, basename='session-assignmentfeedback')
router_sessions.register(r'language', LanguageFeedbackViewSet, basename="session-language")
router_sessions.register(r"languagevote", LanguageFeedbackVoteViewset, basename="session-languagevote")
router_sessions.register(r"metafiltervalue", MetaFilterValueViewSet, basename="session-metafiltervalue")

urlpatterns = [
    path('rest/', include(router.urls)),
    path('rest/', include(router_sessions.urls)),
    path('rest/', include(router_page.urls)),
    path('rest/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('rest/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path("out/<id>/<property>/",  route_outgoing, name="route_outgoing"),
    re_path("data/(?P<version>[0-9]+)", route_data, name="route_data"),
    path("admin", admin.site.urls)
   
] + static(STATIC_URL, document_root=STATIC_ROOT,show_indexes=True) + ([path('silk/', include('silk.urls', namespace='silk'))] if ENABLE_PROFILING else []) + ([path("admin", admin.site.urls)] if DEBUG else [])