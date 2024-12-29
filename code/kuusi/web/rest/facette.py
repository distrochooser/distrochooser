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


from web.models import Facette, Session, FacetteAssignment
from rest_framework import serializers
from drf_spectacular.utils import  extend_schema, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, OpenApiResponse
from rest_framework import status
from kuusi.settings import LANGUAGE_CODES
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_field

from typing import Dict, Any, List

class FacetteAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacetteAssignment
        fields = ('id', 'choosables', 'catalogue_id', 'long_description', 'assignment_type', )

class FacetteSerializer(serializers.ModelSerializer):
    selectable_description = serializers.SerializerMethodField()
    assignments = serializers.SerializerMethodField()
    class Meta:
        model = Facette
        fields = ('id', 'topic', 'selectable_description', 'assignments')
    def get_selectable_description(self, obj: Facette) -> str:
        session: Session = Session.objects.filter(result_id=self.context['session_pk']).first()
        return obj.__("selectable_description",  session.language_code)
    
    @extend_schema_field(field=FacetteAssignmentSerializer(many=True))
    def get_assignments(self, obj:Facette) -> List[FacetteAssignment]:
        serializer = FacetteAssignmentSerializer(
            FacetteAssignment.objects.filter(facettes__in=[obj]),
            many=True
        )
        return serializer.data
    
    
class FacetteViewSet(ListModelMixin, GenericViewSet):
    queryset = Facette.objects.all()
    serializer_class = FacetteSerializer
    @extend_schema(
        responses={
            status.HTTP_200_OK: OpenApiResponse(response=FacetteSerializer, description="The list of Facettes available to use"),
        },
        parameters=[ 
          OpenApiParameter("topic", OpenApiTypes.STR, OpenApiParameter.QUERY,description="The topic of the facettes", required=True),
          OpenApiParameter("session_pk", OpenApiTypes.STR, OpenApiParameter.PATH,description="The session resultid", required=True),
        ],
    )
    def list(self, request,  *args, **kwargs):    
        topic =  request.query_params.get('topic')
        results = Facette.objects.filter(topic=topic)
        serializer = FacetteSerializer(
            results,
            many=True
        )
        serializer.context["session_pk"] = kwargs["session_pk"]
        return Response(serializer.data)
