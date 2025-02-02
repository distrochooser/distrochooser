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


from web.models import FacetteSelection, Session, Facette, Page, FacetteSelectionWidget
from web.rest.page import PageSerializer
from rest_framework import serializers
from drf_spectacular.utils import  extend_schema, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, OpenApiResponse
from rest_framework import status
from kuusi.settings import LANGUAGE_CODES
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, DestroyModelMixin
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_field
from typing import List

class FacetteSelectionSerializer(serializers.ModelSerializer):
    pages_of_facettes = serializers.SerializerMethodField()
    class Meta:
        model = FacetteSelection
        fields = ('id', 'facette', 'weight', 'pages_of_facettes', )


    def get_pages_of_facettes(self, obj: FacetteSelection) ->List[int]:
        facette = obj.facette

        facette_selection_widgets = FacetteSelectionWidget.objects.filter(topic=facette.topic)
        pages = []
        
        widget: FacetteSelectionWidget 
        for widget in facette_selection_widgets:
            page: Page
            for page in widget.pages.all():
                if page.pk not in pages:
                    pages.append(page.pk)
        
        return pages
    
class FacetteSelectionViewSet(ListModelMixin, GenericViewSet, DestroyModelMixin):
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
        request=None,
        parameters=[
          OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH,description="The selection ID to delete", required=True),
          OpenApiParameter("session_pk", OpenApiTypes.STR, OpenApiParameter.PATH, required=True),
        ]
    ) 
    def destroy(self, request, session_pk, pk):
        # TODO: Make old session immutable

        session: Session = Session.objects.filter(result_id=session_pk).first()
        FacetteSelection.objects.filter(pk=pk).filter(session=session).delete()
        return Response()
    @extend_schema(
        responses={
            status.HTTP_200_OK: OpenApiResponse(response=FacetteSelectionSerializer, description="The created facette selection"),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(response=None, description="Either session or facette are not found"),
            status.HTTP_409_CONFLICT: OpenApiResponse(response=None, description="There is already a given selection with this ID and result Id combination")
        },
        parameters=[ 
          OpenApiParameter("session_pk", OpenApiTypes.STR, OpenApiParameter.PATH, required=True),
          OpenApiParameter("reset", OpenApiTypes.STR, OpenApiParameter.QUERY, required=False, description="Force existing selections on the same topic to be deleted. Used for facette selections bound to radio selections. Values: 'all', 'this'"),
        ],
    )
    def create(self, request, session_pk) -> FacetteSelection:
        session: Session = Session.objects.filter(result_id=session_pk).first()
        facette: Facette = Facette.objects.filter(pk=request.data["facette"]).first()

        if session is None or facette is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        is_reset = str(request.query_params.get('reset')).lower()
        if is_reset:
            if is_reset == "all":
                FacetteSelection.objects.filter(session=session).filter(facette__topic=facette.topic).delete()
            if is_reset == "this":
                FacetteSelection.objects.filter(session=session).filter(facette=facette).delete()
    
        selections = FacetteSelection.objects.filter(session=session).filter(facette=facette)
        if selections.count() != 0:
            return Response(status=status.HTTP_409_CONFLICT)
        
        # TODO: Check behaviour? Status code on error?

        selection = FacetteSelection(
            facette=facette,
            session=session,
            weight=request.data["weight"]
        )
        selection.save()
        serializer = FacetteSelectionSerializer(
            selection,
        )
        serializer.context["session_pk"] = session_pk
        return Response(serializer.data)