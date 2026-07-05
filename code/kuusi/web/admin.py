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

from django.contrib import admin

from web.models import GivenFeedback, MetaFilterValue, Choosable,Feedback, AssignmentFeedback, MetaFilterWidget, LanguageFeedback, Page, FacetteRadioSelectionWidget, HTMLWidget, NavigationWidget, FacetteSelectionWidget, Facette, FacetteBehaviour, SessionVersionWidget, Session, SessionMeta, SessionVersion, FacetteSelection, ResultShareWidget, ResultListWidget, FacetteAssignment, PageMarking, ChoosableMeta

class SessionAdmin(admin.ModelAdmin):
    list_display=("started", "duration", "entry_point", "referrer", "language_code", "result_id", "user_agent", "is_ack", "imported_from_session", )
    def has_change_permission(self, request, obj=None):
        return False
    list_filter = ["is_ack", "language_code", "entry_point"]

class FacetteSelectionAdmin(admin.ModelAdmin):
    list_display=("facette", "weight", "session", "imported_from_answer",)
    def has_change_permission(self, request, obj=None):
        return False

class FacetteAdmin(admin.ModelAdmin):
    list_display = ("catalogue_id","description", "topic" )
    pass

[admin.site.register(*models) for models in [
    (Choosable,),
    (GivenFeedback,),
    (ChoosableMeta,),
    (Page,),
    (HTMLWidget,),
    (NavigationWidget,),
    (FacetteSelectionWidget,),
    (FacetteRadioSelectionWidget,),
    (MetaFilterWidget,),
    (MetaFilterValue,),
    (Facette,FacetteAdmin),
    (FacetteBehaviour,),
    (Session,SessionAdmin),
    (SessionMeta,),
    (SessionVersion,),
    (FacetteSelection,FacetteSelectionAdmin),
    (ResultShareWidget,),
    (ResultListWidget,),
    (SessionVersionWidget,),
    (FacetteAssignment,),
    (PageMarking,),
    (Feedback,),
    (AssignmentFeedback,),
    (LanguageFeedback,),
]]