"""
distrochooser
Copyright (C) 2014-2026 Christoph Müller <mail@chmr.eu>

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

from collections import OrderedDict
from json import loads
from typing import Any, Dict, List

from django.core.cache import cache
from django.db.models import Q
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiParameter, OpenApiResponse,
                                   PolymorphicProxySerializer, extend_schema,
                                   extend_schema_field)
from kuusi.settings import WEIGHT_MAP
from rest_framework import serializers, status
from rest_framework.fields import CharField
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.serializers import ListSerializer
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList
from rest_framework.viewsets import GenericViewSet
from web.models import (Choosable, Facette, FacetteAssignment,
                        FacetteRadioSelectionWidget, FacetteSelection,
                        FacetteSelectionWidget, FeedbackWidget, HTMLWidget,
                        MetaFilterValue, MetaFilterWidget, NavigationWidget,
                        Page, ResultListWidget, ResultShareWidget, Session,
                        SessionVersion, SessionVersionWidget, Widget)
from web.rest.choosable import (CHOOSABLE_SERIALIZER_BASE_FIELDS,
                                ChoosableSerializer)
from web.rest.facette import FacetteAssignmentSerializer, FacetteSerializer
from web.rest.session import SessionVersionSerializer

WIDGET_SERIALIZER_BASE_FIELDS = (
    "id",
    "row",
    "col",
    "width",
    "pages",
    "widget_type",
)


# TODO: For all serializers
# MOve the render features into the serializers
# E. g. selections needed facettes, question texts, hints ....
class WidgetSerializer(serializers.ModelSerializer):
    widget_type = serializers.SerializerMethodField()

    class Meta:
        model = Widget
        fields = WIDGET_SERIALIZER_BASE_FIELDS

    def get_widget_type(self, obj):
        return obj.widget_type


class HTMLWidgetSerializer(WidgetSerializer):
    widget_type = serializers.SerializerMethodField()

    class Meta:
        model = HTMLWidget
        fields = WIDGET_SERIALIZER_BASE_FIELDS + ("template",)


class WithFacetteWidgetSerializer(WidgetSerializer):
    facettes = serializers.SerializerMethodField()

    @extend_schema_field(field=FacetteSerializer(many=True))
    def get_facettes(self, obj: FacetteSelectionWidget) -> ReturnList | ReturnDict | Any:
        facettes = Facette.objects.filter(topic=obj.topic)

        serializer = FacetteSerializer(facettes, many=True)
        serializer.context["session"] = self.context["session"]
        return serializer.data


class FacetteSelectionWidgetSerializer(WithFacetteWidgetSerializer):

    class Meta:
        model = FacetteSelectionWidget
        fields = WIDGET_SERIALIZER_BASE_FIELDS + ("topic", "facettes")


class FacetteRadioSelectionWidgetSerializer(WithFacetteWidgetSerializer):

    class Meta:
        model = FacetteRadioSelectionWidget
        fields = WIDGET_SERIALIZER_BASE_FIELDS + ("topic", "facettes")


class MetaFilterWidgetSerializer(WidgetSerializer):
    structure = serializers.SerializerMethodField()
    options = serializers.SerializerMethodField()

    class Meta:
        model = MetaFilterWidget
        fields = WIDGET_SERIALIZER_BASE_FIELDS + (
            "structure",
            "options",
        )

    @extend_schema_field(field=ListSerializer(child=ListSerializer(child=CharField())))
    def get_structure(self, obj: MetaFilterWidget) -> List[str]:
        if not obj.structure:
            return []
        return list(loads(obj.structure))

    def get_options(self, obj: MetaFilterWidget) -> Dict[str, List[str]]:
        return {"archs": ["apple-silicon", "arm", "x86", "x86_64"]}


class SessionVersionWidgetSerializer(WidgetSerializer):
    versions = serializers.SerializerMethodField()

    class Meta:
        model = SessionVersionWidget
        fields = WIDGET_SERIALIZER_BASE_FIELDS + ("versions",)

    @extend_schema_field(field=SessionVersionSerializer(many=True))
    def get_versions(self, obj: SessionVersionWidget) -> ReturnList | ReturnDict | Any:
        serializer = SessionVersionSerializer(SessionVersion.objects.all(), many=True)

        serializer.context["session"] = self.context["session"]
        return serializer.data


class NavigationWidgetSerializer(WidgetSerializer):

    class Meta:
        model = NavigationWidget
        fields = WIDGET_SERIALIZER_BASE_FIELDS


class ResultShareWidgetSerializer(WidgetSerializer):

    class Meta:
        model = ResultShareWidget
        fields = WIDGET_SERIALIZER_BASE_FIELDS


class FeedbackWidgetSerializer(WidgetSerializer):

    class Meta:
        model = FeedbackWidget
        fields = WIDGET_SERIALIZER_BASE_FIELDS


class RankedChoosableSerializer(ChoosableSerializer):
    rank = serializers.SerializerMethodField()
    assignments = serializers.SerializerMethodField()

    class Meta:
        model = Choosable
        fields = CHOOSABLE_SERIALIZER_BASE_FIELDS + ("rank", "assignments")

    def get_rank(self, obj: Choosable) -> int:
        return self.context["score_map"][obj.pk]["SCORE"] if obj.pk in  self.context["score_map"] else 999999999

    def get_description(self, obj: Choosable) -> str:
        session = self.context["session"]
        return obj.__("description", session.language_code)

    @extend_schema_field(field=FacetteAssignmentSerializer(many=True))
    def get_assignments(self, obj: Choosable) -> ReturnList | ReturnDict | Any:
        # A choosable _might_ not have any assingments -> overrule
        serializer = FacetteAssignmentSerializer(
            (
                self.context["assignments"][obj.pk]
                if obj.pk in self.context["assignments"]
                else []
            ),
            many=True,
        )
        serializer.context["session"] = self.context["session"]
        serializer.context["weight_map"] = self.context["weight_map"]
        return serializer.data


class ResultListWidgetSerializer(WidgetSerializer):
    choosables = serializers.SerializerMethodField()

    class Meta:
        model = ResultListWidget
        fields = WIDGET_SERIALIZER_BASE_FIELDS + ("choosables",)

    @extend_schema_field(field=RankedChoosableSerializer(many=True))
    def get_choosables(self, obj: ResultListWidget) -> ReturnList | Any | ReturnDict:
        session = self.context["session"]
        choosables = Choosable.objects.all()
        meta_filter_widgets = MetaFilterWidget.objects.all()
        selections = FacetteSelection.objects.filter(session=session)
        assignments_results = {}
        assignments_weight_map = {}
        stored_meta_filter_values = MetaFilterValue.objects.filter(session=session)
        score_map = {}

        selected_facettes = selections.values_list("facette", flat=True)
        assignments = FacetteAssignment.objects.filter(
            Q(facettes__in=selected_facettes) &
            Q(is_invalidated=False)
        )
        results = []
        for choosable in choosables:
            if choosable.pk not in assignments_results:
                assignments_results[choosable.pk] = []
            # Step 1: Get Assignments from given Facettes
            choosable_assignments = assignments.filter(choosables__in=[choosable])
            for assignment in choosable_assignments:
                # FIXME: The facettes must be at some point converted to a many to one field
                selection = selections.get(
                    facette = assignment.facettes.first(),
                )     
                selection_weight_key = selection.weight
                selection_weight_value = WEIGHT_MAP[selection_weight_key]
                
                assignments_results[choosable.pk].append(assignment)
                assignments_weight_map[assignment.pk] = selection_weight_value
                

            # Step 2: Get Assignments from given Meta filters
            if stored_meta_filter_values.count() > 0:
                for meta_filter_widget in meta_filter_widgets:
                    for meta_filter_widget in meta_filter_widgets:
                        meta_results = (
                            meta_filter_widget.get_assignments_for_meta_values(
                                stored_meta_filter_values,
                                choosable,
                                assignments_results,
                                session,
                            )
                        )
                        if meta_results is not None:
                            if choosable.pk not in assignments_results:
                                assignments_results[choosable.pk] = []
                            assignments_results[choosable.pk].append(meta_results)

            # Step 3: Calculate final scores
            choosable_scores = FacetteAssignment.AssignmentType.get_score_map()
            if choosable.pk in assignments_results:
                assignments_this_choosable = assignments_results[choosable.pk]
                for assignment in assignments_this_choosable:
                    assignment_type = assignment.assignment_type
                    choosable_scores[assignment_type] += 1
                    score_map = {
                        FacetteAssignment.AssignmentType.POSITIVE: 1.2,
                        FacetteAssignment.AssignmentType.NEGATIVE: -0.9,
                        FacetteAssignment.AssignmentType.NEUTRAL: 0,
                        FacetteAssignment.AssignmentType.BLOCKING: -100,
                    }
                    choosable_scores["SCORE"] += choosable_scores[assignment_type] * score_map[assignment_type]

                score_map[choosable.pk] = choosable_scores
                results.append(choosable)


        serializer = RankedChoosableSerializer(results, many=True)
        serializer.context["session"] = session
        serializer.context["score_map"] = score_map
        serializer.context["assignments"] = assignments_results
        serializer.context["weight_map"] = assignments_weight_map

        return serializer.data


class WidgetViewSet(ListModelMixin, GenericViewSet):
    queryset = Page.objects.all()
    @extend_schema(
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=PolymorphicProxySerializer(
                    serializers=[
                        HTMLWidgetSerializer,
                        NavigationWidgetSerializer,
                        SessionVersionWidgetSerializer,
                        FacetteRadioSelectionWidgetSerializer,
                        FacetteSelectionWidgetSerializer,
                        ResultListWidgetSerializer,
                        ResultShareWidgetSerializer,
                        FeedbackWidgetSerializer,
                        MetaFilterWidgetSerializer,
                    ],
                    component_name="MetaWidget",
                    resource_type_field_name="widget_type",
                    many=True,
                ),
                description="The list of widgets available to use",
            ),
        },
        parameters=[
            OpenApiParameter(
                "session_pk",
                OpenApiTypes.STR,
                OpenApiParameter.PATH,
                description="The session resultid",
                required=True,
            ),
            OpenApiParameter(
                "page_pk",
                OpenApiTypes.NUMBER,
                OpenApiParameter.PATH,
                description="The page id",
                required=True,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):

        page_pk = kwargs.get("page_pk")
        cache_key = f"page-{page_pk}-widget"
        session: Session = Session.objects.get(result_id=kwargs["session_pk"])
        obj: Page | None = None
        if page_pk:
            obj = Page.objects.filter(pk=page_pk).first()
        result = []
        # IMPORTANT
        # The serializers are ordered, specialized before generic

        serializers = OrderedDict(
            {
                HTMLWidget: HTMLWidgetSerializer,
                NavigationWidget: NavigationWidgetSerializer,
                SessionVersionWidget: SessionVersionWidgetSerializer,
                FacetteRadioSelectionWidget: FacetteRadioSelectionWidgetSerializer,
                FacetteSelectionWidget: FacetteSelectionWidgetSerializer,
                ResultListWidget: ResultListWidgetSerializer,
                ResultShareWidget: ResultShareWidgetSerializer,
                FeedbackWidget: FeedbackWidgetSerializer,
                MetaFilterWidget: MetaFilterWidgetSerializer,
            }
        )
        # Check if the detail results _can_ be ignored
        # TODO: Increase performance
        ignore_cache_serializers = [ResultListWidget]
        ignore_cache = False
        if obj:
            widget: Widget
            for widget in obj.widget_list:
                for key in ignore_cache_serializers:
                    if isinstance(widget, key):
                        ignore_cache = True
                        break

            if not ignore_cache:
                cache_data = cache.get(cache_key)
                if cache_data is not None:
                    return Response(cache_data)

            widget: Widget
            for widget in obj.widget_list:
                for key, value in serializers.items():
                    if isinstance(widget, key):
                        selected_serializer = value
                        results = selected_serializer(widget)
                        results.context["session"] = session
                        result.append(results.data)
                        break

            cache.set(cache_key, result)

        return Response(result)
