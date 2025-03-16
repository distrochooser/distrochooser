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


from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiParameter, OpenApiResponse,
                                   extend_schema)
from rest_framework import serializers, status
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from web.models import GivenFeedback, Session
from web.rest.hooks import fire_hook


class CreateGivenFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = GivenFeedback
        fields = ('session', 'text')

class GivenFeedbackSerializer(CreateGivenFeedbackSerializer):
    class Meta:
        model = GivenFeedback
        fields = ('text',)


class GivenFeedbackViewset(GenericViewSet):
    queryset = GivenFeedback.objects.all()
    serializer_class = GivenFeedbackSerializer

    @extend_schema(
        request=CreateGivenFeedbackSerializer,
        parameters=[ 
          OpenApiParameter("session_pk", OpenApiTypes.STR, OpenApiParameter.PATH,description="The session resultid", required=True),
        ],
        responses={
            status.HTTP_200_OK: GivenFeedbackSerializer,
        }
    ) 
    def create(self, request, session_pk) -> CreateGivenFeedbackSerializer:
        data = request.data
        text = data["text"]
        session: Session = Session.objects.filter(result_id=session_pk).first()

       
        GivenFeedback.objects.filter(
            session=session
        ).delete()
        
        result = GivenFeedback(
            session=session,
            text=text
        )
        result.save()

        fire_hook(text, session, "💬 Text Feedback", 15545396)

        serializer = GivenFeedbackSerializer(
            result
        )

        serializer.context["session_pk"] = session_pk
        return Response(serializer.data)