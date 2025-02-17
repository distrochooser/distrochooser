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


from web.models import Facette, Session, FacetteAssignment, Choosable, Feedback, AssignmentFeedback
from web.rest.choosable import ChoosableSerializer
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
from rest_framework.serializers import ListSerializer
from rest_framework.fields import IntegerField

from typing import Dict, Any, List


class CreateFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('id', 'choosable', 'assignment', 'is_positive',)

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('id', 'choosable', 'assignment', 'is_positive', 'session')


class AssignmentFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentFeedback
        fields = ('id', 'assignment', 'is_positive', 'session')


class AssignmentFeedbackViewSet(ListModelMixin, GenericViewSet):
    queryset = AssignmentFeedback.objects.all()
    serializer_class = AssignmentFeedbackSerializer
    @extend_schema(
        responses={
            status.HTTP_200_OK: OpenApiResponse(response=AssignmentFeedbackSerializer, description="The list of assignment feedback available to use"),
        },
        parameters=[ 
          OpenApiParameter("session_pk", OpenApiTypes.STR, OpenApiParameter.PATH,description="The session resultid", required=True),
        ],
    )
    def list(self, request,  *args, **kwargs):    
        results = AssignmentFeedback.objects.all()
        serializer = AssignmentFeedbackSerializer(
            results,
            many=True
        )
        serializer.context["session_pk"] = kwargs["session_pk"]
        return Response(serializer.data)

    @extend_schema(
        request=AssignmentFeedbackSerializer,
        parameters=[ 
          OpenApiParameter("session_pk", OpenApiTypes.STR, OpenApiParameter.PATH,description="The session resultid", required=True),
        ],
        responses={
            status.HTTP_200_OK: AssignmentFeedbackSerializer,
        }
    ) 
    def create(self, request, session_pk) -> Feedback:

        data = request.data
        assignment = data["assignment"]
        is_positive = data["is_positive"]
        session: Session = Session.objects.filter(result_id=session_pk).first()
        has_old = AssignmentFeedback.objects.filter(assignment__pk=assignment).filter(session=session).count() > 0

        if has_old:
             AssignmentFeedback.objects.filter(assignment__pk=assignment).delete()

        assignment_obj = FacetteAssignment.objects.filter(pk=assignment).first()
        result = AssignmentFeedback(
            assignment=assignment_obj,
            is_positive=is_positive,
            session=session
        )
        result.save()

        serializer = AssignmentFeedbackSerializer(
            result
        )

        serializer.context["session_pk"] = session_pk
        return Response(serializer.data)
    

    @extend_schema(
        request=None,
        parameters=[
          OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH,description="The feedback ID to delete", required=True),
          OpenApiParameter("session_pk", OpenApiTypes.STR, OpenApiParameter.PATH, required=True),
        ]
    ) 
    def destroy(self, request, session_pk, pk):
        session: Session = Session.objects.filter(result_id=session_pk).first()
        AssignmentFeedback.objects.filter(pk=pk).filter(session=session).delete()
        return Response()
    

class FeedbackViewSet(ListModelMixin, GenericViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    @extend_schema(
        responses={
            status.HTTP_200_OK: OpenApiResponse(response=FeedbackSerializer, description="The list of Facettes available to use"),
        },
        parameters=[ 
          OpenApiParameter("session_pk", OpenApiTypes.STR, OpenApiParameter.PATH,description="The session resultid", required=True),
        ],
    )
    def list(self, request,  *args, **kwargs):    
        results = Feedback.objects.filter(session__result_id=kwargs["session_pk"])
        serializer = FeedbackSerializer(
            results,
            many=True
        )
        serializer.context["session_pk"] = kwargs["session_pk"]
        return Response(serializer.data)

    @extend_schema(
        request=CreateFeedbackSerializer,
        parameters=[ 
          OpenApiParameter("session_pk", OpenApiTypes.STR, OpenApiParameter.PATH,description="The session resultid", required=True),
        ],
        responses={
            status.HTTP_200_OK: FeedbackSerializer,
        }
    ) 
    def create(self, request, session_pk) -> Feedback:

        data = request.data
        choosable = data["choosable"]
        assignment = data["assignment"]
        is_positive = data["is_positive"]
        session: Session = Session.objects.filter(result_id=session_pk).first()
        has_old = Feedback.objects.filter(choosable__pk=choosable).filter(assignment__pk=assignment).filter(session=session).count() > 0

        if has_old:
             Feedback.objects.filter(choosable__pk=choosable).filter(assignment__pk=assignment).delete()
        result = Feedback(
            choosable=Choosable.objects.filter(pk=choosable).first(),
            assignment=FacetteAssignment.objects.filter(pk=assignment).first(),
            is_positive=is_positive,
            session=session
        )
        result.save()

        serializer = FeedbackSerializer(
            result
        )

        serializer.context["session_pk"] = session_pk
        return Response(serializer.data)
    

    @extend_schema(
        request=None,
        parameters=[
          OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH,description="The selection ID to delete", required=True),
          OpenApiParameter("session_pk", OpenApiTypes.STR, OpenApiParameter.PATH, required=True),
        ]
    ) 
    def destroy(self, request, session_pk, pk):
        session: Session = Session.objects.filter(result_id=session_pk).first()
        Feedback.objects.filter(pk=pk).filter(session=session).delete()
        return Response() 

class FacetteAssignmentSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    weight = serializers.SerializerMethodField()
    votes = serializers.SerializerMethodField()
    class Meta:
        model = FacetteAssignment
        fields = ('id', 'choosables', 'catalogue_id', 'description', 'assignment_type', 'weight', 'votes', )

    def get_description(self, obj: FacetteAssignment):
        session: Session = Session.objects.filter(result_id=self.context['session_pk']).first()
        return obj.__("long_description",  session.language_code)
    
    @extend_schema_field(
        field=ListSerializer(
            child=ListSerializer(
                child=IntegerField()
            )
        )
    )
    def get_votes(self, obj: FacetteAssignment):
        return obj.get_votes()

    def get_weight(self, obj: FacetteAssignment) -> int:
        weight_value = None
        if "weight_map" in self.context and obj.pk in self.context["weight_map"]:
            weight_value = self.context["weight_map"][obj.pk]
        return weight_value




class FacetteSerializer(serializers.ModelSerializer):
    selectable_description = serializers.SerializerMethodField()
    assignments = serializers.SerializerMethodField()
    class Meta:
        model = Facette
        fields = ('id', 'topic', 'selectable_description', 'assignments',)
    def get_selectable_description(self, obj: Facette) -> str:
        return obj.get_msgd_id_of_field("selectable_description") 

    @extend_schema_field(field=FacetteAssignmentSerializer(many=True))
    def get_assignments(self, obj:Facette) -> List[FacetteAssignment]:
        serializer = FacetteAssignmentSerializer(
            FacetteAssignment.objects.filter(facettes__in=[obj]),
            many=True
        )
        serializer.context["session_pk"] = self.context["session_pk"]
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
