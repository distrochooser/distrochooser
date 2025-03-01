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


from django.db.models import Q
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiParameter, OpenApiResponse,
                                   extend_schema)
from rest_framework import serializers, status
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from web.models import FacetteBehaviour, FacetteSelection, Session


class FacetteBehaviourSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacetteBehaviour
        fields = ('description', 'criticality', 'affected_objects', 'affected_subjects', )
    
    
class FacetteBehaviourViewSet(ListModelMixin, GenericViewSet):
    queryset = FacetteSelection.objects.all()
    serializer_class = FacetteBehaviourSerializer
    @extend_schema(
        responses={
            status.HTTP_200_OK: OpenApiResponse(response=FacetteBehaviourSerializer, description="The list of active facette behaviour objects"),
        },
        parameters=[ 
          OpenApiParameter("session_pk", OpenApiTypes.STR, OpenApiParameter.PATH, required=True),
        ],
    )
    def list(self, request,  *args, **kwargs):    
        session: Session = Session.objects.filter(result_id=kwargs["session_pk"]).first()
        active_facette_selections = FacetteSelection.objects.filter(session=session)
        results = []
        for active_facette_selection in active_facette_selections:
            facette = active_facette_selection.facette
            behaviours = FacetteBehaviour.objects.filter(
                Q(affected_subjects__pk__in=[facette.pk])|
                Q(affected_objects__pk__in=[facette.pk])
            )
            # TODO: Identify others
            behaviour: FacetteBehaviour
            for behaviour in behaviours:
                result = behaviour.is_true(facette, [])
                if result:
                    results.append(behaviour)

        serializer = FacetteBehaviourSerializer(
            results,
            many=True
        )
        serializer.context["session_pk"] = kwargs["session_pk"]
        return Response(serializer.data)
    
