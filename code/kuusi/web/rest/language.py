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

from typing import List

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_field,
)
from rest_framework import serializers, status
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from web.models import LanguageFeedback, LanguageFeedbackVote, Session
from web.rest.languagevote import LanguageFeedbackVoteSerializer
from web.rest.hooks import fire_hook
from django.core.cache import cache


class CreateLanguageFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageFeedback
        fields = (
            "id",
            "language_key",
            "value",
            "voter_id"
        )


class LanguageFeedbackSerializer(serializers.ModelSerializer):
    votes = serializers.SerializerMethodField()

    class Meta:
        model = LanguageFeedback
        fields = ("id", "session", "language_key", "value", "votes", "voter_id")

    @extend_schema_field(field=LanguageFeedbackVoteSerializer(many=True))
    def get_votes(self, obj: LanguageFeedback) -> List[LanguageFeedbackVote]:
        objects = LanguageFeedbackVote.objects.filter(language_feedback=obj)

        serializer = LanguageFeedbackVoteSerializer(objects, many=True)
        return serializer.data


class LanguageFeedbackViewSet(ListModelMixin, GenericViewSet):
    queryset = LanguageFeedback.objects.all()
    serializer_class = LanguageFeedbackSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=LanguageFeedbackSerializer,
                description="The list of Language feedbacks available",
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
                "voter_id",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description="A optional voter id to identify user owned proposals",
                required=False
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        session: Session = Session.objects.filter(
            result_id=kwargs["session_pk"]
        ).first()
        results = LanguageFeedback.objects.filter(
            session__language_code=session.language_code
        )
        # Censor the other users voter id's, but let the "own"
        # Voter id prevail.
        if "voter_id" in request.query_params:
            for result in results:
                if result.voter_id != request.query_params["voter_id"]:
                    result.voter_id = None
        else:
            for result in results:
                result.voter_id = None

        serializer = LanguageFeedbackSerializer(results, many=True)
        serializer.context["session_pk"] = kwargs["session_pk"]
        return Response(serializer.data)

    @extend_schema(
        request=CreateLanguageFeedbackSerializer,
        parameters=[
            OpenApiParameter(
                "session_pk",
                OpenApiTypes.STR,
                OpenApiParameter.PATH,
                description="The session resultid",
                required=True,
            ),
        ],
        responses={
            status.HTTP_200_OK: LanguageFeedbackSerializer,
        },
    )
    def create(self, request, session_pk) -> LanguageFeedbackSerializer:
        data = request.data
        language_key = data["language_key"]
        value = data["value"]
        voter_id = data["voter_id"]
        session: Session = Session.objects.filter(result_id=session_pk).first()

        # Delete old session proposals or, after reload, old proposals based on the voter id
        LanguageFeedback.objects.filter(session=session).filter(
            language_key=language_key
        ).delete()
        LanguageFeedback.objects.filter(voter_id=voter_id).filter(
            language_key=language_key
        ).delete()

        result = LanguageFeedback(
            language_key=language_key, value=value, session=session, voter_id=voter_id
        )
        result.save()

        fire_hook(f"{language_key} ➡️ {session.language_code} ➡️ {value}", session, "🗣️ Language suggestion", 	2420928)

        serializer = LanguageFeedbackSerializer(result)

        # Clear the cache possibly built by get_translation_haystack
        cache.delete(
           f"translation-{session.language_code}-feedback"
        )

        serializer.context["session_pk"] = session_pk
        return Response(serializer.data)

    @extend_schema(
        request=None,
        parameters=[
            OpenApiParameter(
                "id",
                OpenApiTypes.INT,
                OpenApiParameter.PATH,
                description="The feedback ID to delete",
                required=True,
            ),
            OpenApiParameter(
                "session_pk", OpenApiTypes.STR, OpenApiParameter.PATH, required=True
            ),
        ],
    )
    def destroy(self, request, session_pk, pk):
        session: Session = Session.objects.filter(result_id=session_pk).first()
        LanguageFeedbackSerializer.objects.filter(pk=pk).filter(
            session=session
        ).delete()
        # Clear the cache possibly built by get_translation_haystack
        cache.delete(
           f"translation-{session.language_code}-feedback"
        )
        return Response()
