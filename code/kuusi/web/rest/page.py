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
from web.models import Page, Session, Widget, HTMLWidget, FacetteRadioSelectionWidget, FacetteSelectionWidget, NavigationWidget, ResultListWidget, ResultShareWidget, Facette, SessionVersionWidget, SessionVersion
from web.rest.facette import FacetteSerializer
from web.rest.session import SessionVersionSerializer
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.viewsets import  GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, OpenApiResponse
from drf_spectacular.utils import extend_schema_field, PolymorphicProxySerializer

from collections import OrderedDict
from typing import List, Tuple




class PageSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = '__all__'

    def get_text(self, obj: Page) -> str:
        session: Session = Session.objects.filter(result_id=self.context['session_pk']).first()
        return obj.__("text", session.language_code)
    
    
    
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
        session = sessions.first()
        queryset = Page.objects.all() if not session.version else Page.objects.exclude(not_in_versions__in=[
            session.version
        ])
        
        serializer = PageSerializer(
            queryset,
            many=True
        )

        serializer.context["session_pk"] = kwargs["session_pk"]
        return Response(serializer.data)

