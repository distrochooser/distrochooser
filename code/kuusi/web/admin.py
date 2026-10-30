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
from django.contrib.admin import SimpleListFilter
from kuusi.settings import DEBUG

from web.models import (
    GivenFeedback,
    MetaFilterValue,
    Choosable,
    Feedback,
    AssignmentFeedback,
    MetaFilterWidget,
    LanguageFeedback,
    Page,
    FacetteRadioSelectionWidget,
    HTMLWidget,
    NavigationWidget,
    FacetteSelectionWidget,
    Facette,
    FacetteBehaviour,
    SessionVersionWidget,
    Session,
    SessionMeta,
    SessionVersion,
    FacetteSelection,
    ResultShareWidget,
    ResultListWidget,
    FacetteAssignment,
    PageMarking,
    ChoosableMeta,
    TimeFrame,
    TimeFrameCell,
    TimeFrameRow,
)


class SessionAdmin(admin.ModelAdmin):
    list_display = (
        "started",
        "duration",
        "entry_point",
        "referrer",
        "language_code",
        "result_id",
        "user_agent",
        "is_container_visible",
        "is_ack",
        "import_date_time",
        "imported_from_session",
    )

    def has_change_permission(self, request, obj=None):
        return True

    list_filter = ["is_ack", "language_code", "entry_point", "import_date_time"]


class FacetteSelectionAdmin(admin.ModelAdmin):
    list_display = (
        "facette",
        "weight",
        "session",
        "import_date_time",
        "imported_from_answer",
    )

    def has_change_permission(self, request, obj=None):
        return False

    list_filter = ["imported_from_answer"]


class FacetteAdmin(admin.ModelAdmin):
    list_display = ("catalogue_id", "description", "topic")
    pass


class TimeFrameAdmin(admin.ModelAdmin):
    list_per_page = 12
    list_display = (
        "year",
        "time_frame_type",
        "date",
        "end_date",
        "rank",
        "all_visitors",
        "all_crawlers",
        "all_visitors_of_year",
        "percentage_of_year",
        "results",
        "container_visiblility",
        "daily",
        "duration",
        "worst_result_day",
        "top_result_day",
        "backlinks",
        "top_language_results",
        "top_hit_domain",
        "top_result_domain",
        "top_result_os",
        "top_hit_crawlers",
        "crawler_with_result",
    )
    ordering = ("-time_frame_type", "date")
    list_filter = ["time_frame_type", "date", "year"]


class ZeroAckFilter(SimpleListFilter):

    title = "No ACK"
    parameter_name = "no_ack"

    def lookups(self, request, model_admin):
        return [("True", "True")]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(ack_percentage__gt=0)


class TimeFrameRowAdmin(admin.ModelAdmin):
    list_display = (
        "time_frame",
        "row_type",
        "row_key",
        "ack_percentage",
        "row_value_with_ack",
        "row_value_no_ack",
    )
    list_filter = ["time_frame", "row_type", ZeroAckFilter]


class TimeFrameCellAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "time_frame",
        "key",
        "content",
    )


[
    admin.site.register(*models)
    for models in [
        (TimeFrameCell, TimeFrameCellAdmin),
        (TimeFrame, TimeFrameAdmin),
        (TimeFrameRow, TimeFrameRowAdmin),
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
        (Facette, FacetteAdmin),
        (FacetteBehaviour,),
        (Session, SessionAdmin),
        (SessionMeta,),
        (SessionVersion,),
        (FacetteSelection, FacetteSelectionAdmin),
        (ResultShareWidget,),
        (ResultListWidget,),
        (SessionVersionWidget,),
        (FacetteAssignment,),
        (PageMarking,),
        (Feedback,),
        (AssignmentFeedback,),
        (LanguageFeedback,),
    ]
]
