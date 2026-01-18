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


from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiParameter, OpenApiResponse,
                                   extend_schema)
from rest_framework import serializers, status
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from web.models import LanguageFeedback, LanguageFeedbackVote, Session


class CreateLanguageFeedbackVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageFeedbackVote
        fields = ('language_feedback', 'is_positive','session', 'origin')

class LanguageFeedbackVoteSerializer(CreateLanguageFeedbackVoteSerializer):
    class Meta:
        model = LanguageFeedbackVote
        fields = ('language_feedback', 'is_positive', 'session')


class LanguageFeedbackVoteViewset(ListModelMixin, GenericViewSet):
    queryset = LanguageFeedbackVote.objects.all()
    serializer_class = LanguageFeedbackVote
    @extend_schema(
        responses={
            status.HTTP_200_OK: OpenApiResponse(response=LanguageFeedbackVoteSerializer, description="The list of Language feedbacks votes available for the language extracted from the session language"),
        },
        parameters=[ 
          OpenApiParameter("session_pk", OpenApiTypes.STR, OpenApiParameter.PATH,description="The session resultid", required=True),
        ],
    )
    def list(self, request,  *args, **kwargs):    
        session: Session = Session.objects.filter(result_id=kwargs["session_pk"]).first()
        results = LanguageFeedbackVote.objects.filter(language_feedback__session__language_code=session.language_code)
        serializer = LanguageFeedbackVoteSerializer(
            results,
            many=True
        )
        serializer.context["session_pk"] = kwargs["session_pk"]
        return Response(serializer.data)

    @extend_schema(
        request=CreateLanguageFeedbackVoteSerializer,
        parameters=[ 
          OpenApiParameter("session_pk", OpenApiTypes.STR, OpenApiParameter.PATH,description="The session resultid", required=True),
        ],
        responses={
            status.HTTP_200_OK: CreateLanguageFeedbackVoteSerializer,
        }
    ) 
    def create(self, request, session_pk) -> CreateLanguageFeedbackVoteSerializer:
        data = request.data
        language_feedback = data["language_feedback"]
        is_positive = data["is_positive"]
        origin = data["origin"]

        if origin is not None and  LanguageFeedbackVote.objects.filter(
            language_feedback__pk=language_feedback,
            origin=origin,
            is_positive=is_positive
        ).count() > 0:
            LanguageFeedbackVote.objects.filter(
                language_feedback__pk=language_feedback,
                origin=origin
            ).delete()
        
        session: Session = Session.objects.filter(result_id=session_pk).first()
        LanguageFeedbackVote.objects.filter(
            session=session,
            language_feedback__pk=language_feedback
        ).delete()
        result = LanguageFeedbackVote(
            session=session,
            language_feedback = LanguageFeedback.objects.filter(pk=language_feedback).first(),
            is_positive =is_positive,
            origin=origin
        )
        result.save()

        serializer = LanguageFeedbackVoteSerializer(
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
        LanguageFeedbackVote.objects.filter(pk=pk).filter(language_feedback__session=session).delete()
        return Response()