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


from web.models import Category, Session, Page
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, OpenApiResponse
from web.rest.helper import get_categories_and_filtered_pages

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = '__all__'
    def get_name(self, obj: Category) -> str:
        return obj.get_msgd_id_of_field("name")
    
    
class CategoryViewSet(ListModelMixin, GenericViewSet):
    serializer_class = CategorySerializer
    @extend_schema(
        description="Return the list of pages available to this session",
        responses={
            status.HTTP_200_OK: OpenApiResponse(response=CategorySerializer, description="The list of Pages available to use"),
        },
        parameters=[ 
          OpenApiParameter("session_pk", OpenApiTypes.STR, OpenApiParameter.PATH,description="The session resultid", required=True),
          OpenApiParameter("current_page", OpenApiTypes.STR, OpenApiParameter.QUERY,description="Currently selected PAGE", required=False),
        ],
    )
    def list(self, request,  *args, **kwargs):
        session: Session = Session.objects.filter(result_id=kwargs["session_pk"]).first()
        page_id =  request.query_params.get('page_id')
        if not page_id:
            page = Page.objects.first()
        else:
            page = Page.objects.filter(catalogue_id=page_id)
        _, categories = get_categories_and_filtered_pages(page, session)
       

        serializer = CategorySerializer(
            categories,
            many=True
        )

        serializer.context["session_pk"] = kwargs["session_pk"]
        return Response(serializer.data)

    