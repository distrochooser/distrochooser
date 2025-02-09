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


from web.models import MetaFilterValue, Session
from web.rest.page import PageSerializer
from rest_framework import serializers
from drf_spectacular.utils import  extend_schema, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, OpenApiResponse
from rest_framework import status
from kuusi.settings import LANGUAGE_CODES
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, DestroyModelMixin
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_field
from typing import List

class MetaFilterValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaFilterValue
        fields = ('id', 'key', 'value', )

class CreateMetaFilterValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaFilterValue
        fields = ( 'key', 'value',  )   

class MetaFilterValueViewSet(ListModelMixin, GenericViewSet, DestroyModelMixin):
    queryset = MetaFilterValue.objects.all()
    serializer_class = MetaFilterValueSerializer
    @extend_schema(
        responses={
            status.HTTP_200_OK: OpenApiResponse(response=MetaFilterValueSerializer, description="The list of meta values store within this session"),
        },
        parameters=[ 
          OpenApiParameter("session_pk", OpenApiTypes.STR, OpenApiParameter.PATH, required=True),
        ],
    )
    def list(self, request,  *args, **kwargs):    
        session: Session = Session.objects.filter(result_id=kwargs["session_pk"]).first()
        results = MetaFilterValue.objects.filter(session=session)
        serializer = MetaFilterValueSerializer(
            results,
            many=True
        )
        serializer.context["session_pk"] = kwargs["session_pk"]
        return Response(serializer.data)
    

    @extend_schema(
        request=None,
        parameters=[
          OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH,description="The meta filter value ID to delete", required=True),
          OpenApiParameter("session_pk", OpenApiTypes.STR, OpenApiParameter.PATH, required=True),
        ]
    ) 
    def destroy(self, request, session_pk, pk):
        session: Session = Session.objects.filter(result_id=session_pk).first()
        MetaFilterValue.objects.filter(pk=pk).filter(session=session).delete()
        return Response()

    @extend_schema(
        responses={
            status.HTTP_200_OK: OpenApiResponse(response=MetaFilterValueSerializer, description="The created meta filter value"),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(response=None, description="Session was not found"),
            status.HTTP_406_NOT_ACCEPTABLE: OpenApiResponse(response=None, description="Either key or value are null")
        },
        parameters=[ 
          OpenApiParameter("session_pk", OpenApiTypes.STR, OpenApiParameter.PATH, required=True),
        ],
    )
    def create(self, request, session_pk) -> MetaFilterValue:
        session: Session = Session.objects.filter(result_id=session_pk).first()

        if session is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        key = request.data["key"]
        value = request.data["value"]

        if key is None or value is None:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        MetaFilterValue.objects.filter(session=session).filter(key=key).delete()

        obj = MetaFilterValue(
            key=key,
            session=session,
            value=value
        )
        obj.save()
        serializer = MetaFilterValueSerializer(
            obj,
        )
        serializer.context["session_pk"] = session_pk
        return Response(serializer.data)