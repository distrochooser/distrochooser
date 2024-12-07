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


from web.models import Category, Session, Page
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from kuusi.settings import LANGUAGE_CODES
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, OpenApiResponse

from typing import Dict, Any

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = '__all__'
    def get_name(self, obj: Category) -> str:
        session: Session = Session.objects.filter(result_id=self.context['session_pk']).first()
        return obj.__("name", session.language_code)
    
    
class CategoryViewSet(ListModelMixin, GenericViewSet):
    serializer_class = CategorySerializer
    @extend_schema(
        description="Return the list of pages available to this session",
        responses={
            status.HTTP_200_OK: OpenApiResponse(response=CategorySerializer, description="The list of Pages available to use"),
        },
        parameters=[ 
          OpenApiParameter("current_category", OpenApiTypes.STR, OpenApiParameter.QUERY,description="Currently selected category", required=False),
        ],
    )
    def list(self, request,  *args, **kwargs):
        session: Session = Session.objects.filter(result_id=kwargs["session_pk"]).first()
        all_categories = Category.objects.exclude(target_page__not_in_version=[session.pk]) if session.version else Category.objects.all()
        
        # FIXME: Need helper such as get_page_route in web.py
        # FIXME: Redundancy towards page.py DRF module
        pages = Page.objects.all() if session.version is None else Page.objects.exclude(not_in_versions__in=[session.version])
        version_comp_pages = []
        chained_page: Page
        for chained_page in pages:
            if chained_page.is_visible(session):
                version_comp_pages.append(chained_page)

        categories = []
        for chained_page in pages:
            # Child categories will be created later, when the steps are created.
            used_in_category = Category.objects.filter(
                target_page=chained_page, child_of__isnull=True
            )
            if used_in_category.count() > 0:
                categories.append(used_in_category.first())

        serializer = CategorySerializer(
            categories,
            many=True
        )

        serializer.context["session_pk"] = kwargs["session_pk"]
        return Response(serializer.data)

