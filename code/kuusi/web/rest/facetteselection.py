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


from web.models import FacetteSelection, Session, Facette
from rest_framework import serializers
from drf_spectacular.utils import  extend_schema, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, OpenApiResponse
from rest_framework import status
from kuusi.settings import LANGUAGE_CODES
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response


class FacetteSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacetteSelection
        fields = ('id', 'facette', 'weight')
    
    
class FacetteSelectionViewSet(ListModelMixin, GenericViewSet):
    queryset = FacetteSelection.objects.all()
    serializer_class = FacetteSelectionSerializer
    @extend_schema(
        responses={
            status.HTTP_200_OK: OpenApiResponse(response=FacetteSelectionSerializer, description="The list of facette selections available to use"),
        },
        parameters=[ 
          OpenApiParameter("session_pk", OpenApiTypes.STR, OpenApiParameter.PATH, required=True),
        ],
    )
    def list(self, request,  *args, **kwargs):    
        session: Session = Session.objects.filter(result_id=kwargs["session_pk"]).first()
        results = FacetteSelection.objects.filter(session=session)
        serializer = FacetteSelectionSerializer(
            results,
            many=True
        )
        serializer.context["session_pk"] = kwargs["session_pk"]
        return Response(serializer.data)


    @extend_schema(
        responses={
            status.HTTP_200_OK: OpenApiResponse(response=FacetteSelectionSerializer, description="The created facette selection"),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(response=None, description="Either session or facette are not found")
        },
        parameters=[ 
          OpenApiParameter("session_pk", OpenApiTypes.STR, OpenApiParameter.PATH, required=True),
        ],
    )
    def create(self, request, session_pk):
        session: Session = Session.objects.filter(result_id=session_pk).first()
        facette: Facette = Facette.objects.filter(pk=request.data["facette"]).first()

        if session is None or facette is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # TODO: Store selection
        # TODO: Check behaviour? Status code on error?
        pass