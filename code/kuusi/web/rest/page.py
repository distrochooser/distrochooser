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


from django.shortcuts import get_object_or_404
from web.models import Page, Session, Widget, HTMLWidget, FacetteRadioSelectionWidget, FacetteSelectionWidget, NavigationWidget, ResultListWidget, ResultShareWidget, Facette
from web.rest.facette import FacetteSerializer
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.viewsets import  GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, OpenApiResponse
from drf_spectacular.utils import extend_schema_field, PolymorphicProxySerializer

from typing import List, Tuple

WIDGET_SERIALIZER_BASE_FIELDS = ("id", "row", "col", "width", "pages", "widget_type")

# TODO: For all serializers
# MOve the render features into the serializers
# E. g. selections needed facettes, question texts, hints ....
class WidgetSerializer(serializers.ModelSerializer):
    widget_type = serializers.CharField(default="Widget")
    class Meta:
        model = Widget
        fields = WIDGET_SERIALIZER_BASE_FIELDS
    
    
class HTMLWidgetSerializer(serializers.ModelSerializer):
    widget_type = serializers.CharField(default="HTMLWidget")
    class Meta:
        model = HTMLWidget
        fields = WIDGET_SERIALIZER_BASE_FIELDS + ("template", "widget_type")

class WithFacetteWidgetSerializer(serializers.Serializer):
    facettes = serializers.SerializerMethodField()

    @extend_schema_field(
        field=FacetteSerializer(
            many=True
        )
    )
    def get_facettes(self, obj: FacetteSelectionWidget) -> List[Facette]:
        facettes: Facette = Facette.objects.filter(topic=obj.topic)

        serializer = FacetteSerializer(
            facettes,
            many=True
        )
        serializer.context["session_pk"] = self.context['session_pk']
        return serializer.data

class FacetteSelectionWidgetSerializer(serializers.ModelSerializer, WithFacetteWidgetSerializer):
    widget_type = serializers.CharField(default="FacetteSelectionWidget")
    class Meta:
        model = FacetteSelectionWidget
        fields = WIDGET_SERIALIZER_BASE_FIELDS + ("topic", "facettes")

class FacetteRadioSelectionWidgetSerializer(serializers.ModelSerializer, WithFacetteWidgetSerializer):
    widget_type = serializers.CharField(default="FacetteRadioSelectionWidget")
    class Meta:
        model = FacetteRadioSelectionWidget
        fields = WIDGET_SERIALIZER_BASE_FIELDS + ("topic", "facettes")



class NavigationWidgetSerializer(serializers.ModelSerializer):
    widget_type = serializers.CharField(default="NavigationWidget")
    class Meta:
        model = NavigationWidget
        fields = WIDGET_SERIALIZER_BASE_FIELDS

class ResultShareWidgetSerializer(serializers.ModelSerializer):
    widget_type = serializers.CharField(default="ResultShareWidget")
    class Meta:
        model = ResultShareWidget
        fields = WIDGET_SERIALIZER_BASE_FIELDS

class ResultListWidgetSerializer(serializers.ModelSerializer):
    widget_type = serializers.CharField(default="ResultListWidget")
    class Meta:
        model = ResultListWidget
        fields = WIDGET_SERIALIZER_BASE_FIELDS

class PageSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()
    # https://github.com/axnsan12/drf-yasg/issues/584
    widget_list = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = '__all__'

    def get_text(self, obj: Page) -> str:
        session: Session = Session.objects.filter(result_id=self.context['session_pk']).first()
        return obj.__("text", session.language_code)
    
    # https://github.com/tfranzel/drf-spectacular/issues/382
    @extend_schema_field(
        field=PolymorphicProxySerializer(
            serializers=[
                HTMLWidgetSerializer,
                FacetteRadioSelectionWidgetSerializer,
                FacetteSelectionWidgetSerializer,
                NavigationWidgetSerializer,
                ResultShareWidgetSerializer,
                ResultListWidgetSerializer,
                WidgetSerializer
            ],
            component_name="MetaWidget",
            resource_type_field_name=None,
            many=True
        )
    )
    def get_widget_list(self, obj: Page) -> List[WidgetSerializer | FacetteSelectionWidgetSerializer | FacetteRadioSelectionWidgetSerializer | HTMLWidgetSerializer]:
        result = []
        # IMPORTANT
        # The serializers are ordered, specialized before generic
        serializers = {
            HTMLWidget: HTMLWidgetSerializer,
            FacetteRadioSelectionWidget: FacetteRadioSelectionWidgetSerializer,
            FacetteSelectionWidget: FacetteSelectionWidgetSerializer,
            NavigationWidget: NavigationWidgetSerializer,
            ResultListWidget: ResultListWidgetSerializer,
            ResultShareWidget: ResultShareWidgetSerializer
        }
        widget: Widget
        for widget in obj.widget_list:
            for key, value in serializers.items():
                if isinstance(widget, key):
                    selected_serializer = serializers[type(widget)]
                    results = selected_serializer(
                        widget
                    )
                    results.context["session_pk"] = self.context["session_pk"]
                    result.append(results.data)
                    break
        
        return result
    
    
class PageViewSet(GenericViewSet, ListModelMixin):
    serializer_class = PageSerializer
    @extend_schema(
        request=None,
        parameters=[
          OpenApiParameter("session_pk", OpenApiTypes.STR, OpenApiParameter.PATH,description="The session resultid", required=True),
          OpenApiParameter("id", OpenApiTypes.STR, OpenApiParameter.PATH,description="A result id to retrieve", required=True),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(response=PageSerializer, description="The wanted page object"),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description='The page or session was not found')
        }
    ) 
    def retrieve(self, request, session_pk, pk=None):
        queryset = Page.objects.all()
        session = get_object_or_404(queryset, catalogue_id=pk)
        serializer = PageSerializer(session)
        serializer.context["session_pk"] = session_pk
        return Response(serializer.data)
    
    @extend_schema(
        description="Return the list of pages available to this session",
        responses={
            status.HTTP_200_OK: OpenApiResponse(response=PageSerializer, description="The list of Pages available to use"),
            status.HTTP_412_PRECONDITION_FAILED: OpenApiResponse(description='The session was not found')
        },
        parameters=[ 
          OpenApiParameter("session_pk", OpenApiTypes.STR, OpenApiParameter.PATH,description="The session resultid", required=True),
        ],
    )
    def list(self, request,  *args, **kwargs):
        sessions = Session.objects.filter(result_id=kwargs["session_pk"])
        if sessions.count() == 0:
            return Response(status=status.HTTP_412_PRECONDITION_FAILED)
       
        serializer = PageSerializer(
            Page.objects.all(),
            many=True
        )

        serializer.context["session_pk"] = kwargs["session_pk"]
        return Response(serializer.data)

