from web.models import Choosable
from rest_framework import routers, serializers, viewsets
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, OpenApiResponse
from rest_framework import status
from kuusi.settings import LANGUAGE_CODES
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

class ChoosableSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    class Meta:
        model = Choosable
        fields = ('id', 'name', 'description', 'bg_color', 'fg_color')

    def get_description(self, obj: Choosable) -> str:
        return obj.__("description",  self.context['request'].query_params["lang"])

class ChoosableViewSet(ListModelMixin, GenericViewSet):
    queryset = Choosable.objects.all()
    serializer_class = ChoosableSerializer

    @extend_schema(
        parameters=[
          OpenApiParameter("lang", OpenApiTypes.STR, OpenApiParameter.QUERY,description="The language code to translate this values", required=True),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(response=ChoosableSerializer, description="The list of Choosables available to use"),
            status.HTTP_412_PRECONDITION_FAILED: OpenApiResponse(description='Invalid language'),
        }
    )
    def list(self, request,  *args, **kwargs):
        lang = request.query_params.get('lang')
        if lang not in LANGUAGE_CODES:
            return Response(status=status.HTTP_412_PRECONDITION_FAILED)
        return super().list(request, *args, **kwargs)
