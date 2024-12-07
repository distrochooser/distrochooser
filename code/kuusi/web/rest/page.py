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


from web.models import Page, Session
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from kuusi.settings import LANGUAGE_CODES
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

from typing import Dict, Any

class PageSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()
    class Meta:
        model = Page
        fields = '__all__'
    def get_text(self, obj: Page) -> str:
        session: Session = Session.objects.filter(result_id=self.context['view'].kwargs["sessions_pk"]).first()
        return obj.__("text", session.language_code)
    
    
class PageViewSet(ListModelMixin, GenericViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: OpenApiResponse(response=PageSerializer, description="The list of Pages available to use"),
        }
    )
    def list(self, request,  *args, **kwargs):
        # TODO: Obey versions
        return super().list(request, *args, **kwargs)

