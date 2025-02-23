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

from collections import OrderedDict
from json import loads

from django.shortcuts import render
from django.template import Context, Engine, Template
from web.models import (
    Page,
    Session,
    Widget,
    HTMLWidget,
    FacetteRadioSelectionWidget,
    FacetteSelectionWidget,
    NavigationWidget,
    ResultListWidget,
    ResultShareWidget,
    MetaFilterWidget,
    MetaFilterWidgetElement,
    MetaFilterWidgetStructure,
    MetaFilterValue,
    Facette,
    SessionVersionWidget,
    SessionVersion,
    FacetteSelection,
    Choosable,
    FacetteAssignment,
    Feedback,
)
from web.rest.facette import FacetteSerializer, FacetteAssignmentSerializer
from web.rest.session import SessionVersionSerializer
from web.rest.choosable import ChoosableSerializer, CHOOSABLE_SERIALIZER_BASE_FIELDS
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, OpenApiResponse
from rest_framework import status
from kuusi.settings import LANGUAGE_CODES, WEIGHT_MAP, BASE_DIR, CACHE_TIMEOUT
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.serializers import ListSerializer
from rest_framework.fields import CharField
from time import time
from drf_spectacular.utils import extend_schema_field, PolymorphicProxySerializer

from rest_polymorphic.serializers import PolymorphicSerializer
from django.core.cache import cache
from typing import List
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

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
    def get_facettes(self, obj: FacetteSelectionWidget) -> List[Facette]:
        facettes: Facette = Facette.objects.filter(topic=obj.topic)

        serializer = FacetteSerializer(facettes, many=True)
        serializer.context["session_pk"] = self.context["session_pk"]
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

    class Meta:
        model = MetaFilterWidget
        fields = WIDGET_SERIALIZER_BASE_FIELDS + ("structure",)

    @extend_schema_field(
        field=ListSerializer(
            child=ListSerializer(
                child=CharField()
            )
        )
    )
    def get_structure(self, obj: MetaFilterWidget) -> List[str]:
        return loads(obj.structure)


class SessionVersionWidgetSerializer(WidgetSerializer):
    versions = serializers.SerializerMethodField()

    class Meta:
        model = SessionVersionWidget
        fields = WIDGET_SERIALIZER_BASE_FIELDS + ("versions",)

    @extend_schema_field(field=SessionVersionSerializer(many=True))
    def get_versions(self, obj: SessionVersionWidget) -> List[SessionVersion]:
        serializer = SessionVersionSerializer(SessionVersion.objects.all(), many=True)

        serializer.context["session_pk"] = self.context["session_pk"]
        return serializer.data


class NavigationWidgetSerializer(WidgetSerializer):

    class Meta:
        model = NavigationWidget
        fields = WIDGET_SERIALIZER_BASE_FIELDS


class ResultShareWidgetSerializer(WidgetSerializer):

    class Meta:
        model = ResultShareWidget
        fields = WIDGET_SERIALIZER_BASE_FIELDS


class RankedChoosableSerializer(ChoosableSerializer):
    rank = serializers.SerializerMethodField()
    assignments = serializers.SerializerMethodField()

    class Meta:
        model = Choosable
        fields = CHOOSABLE_SERIALIZER_BASE_FIELDS + ("rank", "assignments")

    def get_rank(self, obj: Choosable) -> int:
        return (
            self.context["ranking"][obj.pk]
            if obj.pk in self.context["ranking"]
            else 9999999999
        )

    def get_description(self, obj: Choosable) -> str:
        session = Session.objects.filter(result_id=self.context["session_pk"]).first()
        return obj.__("description", session.language_code)

    @extend_schema_field(field=FacetteAssignmentSerializer(many=True))
    def get_assignments(self, obj: Choosable) -> List[FacetteAssignment]:
        serializer = FacetteAssignmentSerializer(
            self.context["assignments"][obj.pk], many=True
        )
        serializer.context["session_pk"] = self.context["session_pk"]
        serializer.context["weight_map"] = self.context["weight_map"]
        return serializer.data


class ResultListWidgetSerializer(WidgetSerializer):
    choosables = serializers.SerializerMethodField()

    class Meta:
        model = ResultListWidget
        fields = WIDGET_SERIALIZER_BASE_FIELDS + ("choosables",)

    @extend_schema_field(field=RankedChoosableSerializer(many=True))
    def get_choosables(self, obj: ResultListWidget) -> List[Choosable]:
        session = Session.objects.filter(result_id=self.context["session_pk"]).first()
        choosables = Choosable.objects.all()
        meta_filter_widgets = MetaFilterWidget.objects.all()
        facette_assignments = FacetteAssignment.objects.all()
        selections = FacetteSelection.objects.filter(session=session)
        ranking = {}
        assignments_results = {}
        assignments_weight_map = {}
        stored_meta_filter_values = MetaFilterValue.objects.filter(session=session)
        feedback_in_session = Feedback.objects.filter(session=session)

        for choosable in choosables:
            scores_by_type = FacetteAssignment.AssignmentType.get_score_map_by_type()
            assignments_results[choosable.pk] = []
            assignments_weight_map = {}
            
            assignments_with_choosable = facette_assignments.filter(choosables__in=[choosable])
   
            for selection in selections:
                facette = selection.facette
                selection_weight_key = selection.weight
                selection_weight_value = WEIGHT_MAP[selection_weight_key]
                # TODO: Decicide what to to with feedback relating to assignments, but not yet mapped to them.
                
                assignments_stored = assignments_with_choosable.filter(
                    facettes__in=[facette]
                )
                assignments = list(assignments_stored)
                # Append "virtual" assignments caused by stored meta values
                # TODO: Decide to append these also when no selection was given
    
                for meta_filter_widget in meta_filter_widgets:
                    results = meta_filter_widget.get_virtual_assignments(stored_meta_filter_values, choosable)
                    if results.__len__() != 0:
                        assignments = assignments + results

                for assignment in assignments:
                    # Don't collect assignments twice
                    is_assignment_collected = len(list(filter(lambda l: l.catalogue_id == assignment.catalogue_id, assignments_results[choosable.pk]))) == 0
                    if is_assignment_collected:
                        # Only include assignments without negative user feedback
                        has_negative_feedback = (
                            feedback_in_session
                            .filter(assignment=assignment)
                            .filter(choosable=choosable)
                            .count()
                            > 0
                        )
                        # FIXME: Prevent the virtual assignments from getting weighted
                        if not has_negative_feedback:
                            weighted_score = 1 * selection_weight_value
                            scores_by_type[assignment.assignment_type] += weighted_score
                        assignments_results[choosable.pk].append(assignment)

                        assignments_weight_map[assignment.pk] = selection_weight_value
            
            ranking[choosable.pk] = FacetteAssignment.AssignmentType.get_score(
                scores_by_type
            )

        serializer = RankedChoosableSerializer(choosables, many=True)
        serializer.context["session_pk"] = self.context["session_pk"]
        serializer.context["ranking"] = ranking
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
        obj: Page = None
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
                MetaFilterWidget: MetaFilterWidgetSerializer,
            }
        )

        # Check if the detail results _can_ be ignored
        # TODO: Increase performance
        ignore_cache_serializers = [ResultListWidget]
        ignore_cache = False
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
                    selected_serializer = serializers[type(widget)]
                    results = selected_serializer(widget)
                    results.context["session_pk"] = kwargs["session_pk"]
                    result.append(results.data)
                    break
        
        cache.set(cache_key, result)

        return Response(result)
