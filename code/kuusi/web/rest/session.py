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


from web.models import Session, SessionMeta, FacetteSelection, Facette, SessionVersion, LanguageFeedback, MetaFilterValue
from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, OpenApiResponse
from rest_framework import status
from kuusi.settings import LANGUAGE_CODES, DEFAULT_SESSION_META, FRONTEND_URL, KUUSI_ICON, RTL_LANGUAGES, KUUSI_NAME, KUUSI_LOGO, KUUSI_META_TAGS, LOCALE_MAPPING
from web.models import TRANSLATIONS, Feedback
from web.models.translateable import get_translation_haystack
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from django.shortcuts import get_object_or_404

from typing import Dict, Any, List

class SessionSerializer(serializers.ModelSerializer):
    session_origin = serializers.SerializerMethodField()
    language_codes = serializers.SerializerMethodField()
    language_values = serializers.SerializerMethodField()
    is_language_rtl = serializers.SerializerMethodField()
    base_url = serializers.CharField(default=FRONTEND_URL)
    name = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()
    meta = serializers.SerializerMethodField()
    icon = serializers.SerializerMethodField()
    class Meta:
        model = Session
        fields = ('id', 'result_id', 'language_code', 'language_codes',  'session_origin', 'started', 'version', 'base_url', 'language_values', 'is_language_rtl', 'name', 'logo', 'meta', 'icon')

    def get_session_origin(self, obj: Session) -> str:
        return obj.session_origin.result_id if obj.session_origin else None
    
    def get_language_codes(self, obj: Session) -> Dict[str, str]:
        return LANGUAGE_CODES

    def get_language_values(self, obj:Session) -> Dict[str, str]:
        return get_translation_haystack(obj.language_code)

    def get_is_language_rtl(self, obj: Session) -> bool:
        return obj.language_code in RTL_LANGUAGES
    
    def get_logo(self, obj: Session) -> str:
        return KUUSI_LOGO
    
    def get_name(self, obj: Session) -> str:
        return KUUSI_NAME
    
    def get_icon(self, obj: Session) -> str:
        return KUUSI_ICON
    
    def get_meta(self, obj: Session) -> Dict[str, any]:
        meta =  KUUSI_META_TAGS.copy()
        meta["og:locale"] = LOCALE_MAPPING[obj.language_code]
        return meta


class SessionVersionSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()
    class Meta:
        model = SessionVersion
        fields = '__all__' 

    def get_text(self, obj: SessionVersion) -> str:
        session: Session = Session.objects.filter(result_id=self.context['session_pk']).first()
        return obj.__("version_name", session.language_code)


class SessionViewSet(ViewSet):
    serializer_class = Session
    queryset = Session.objects.all()    


    @extend_schema(
        request=None,
        parameters=[
          OpenApiParameter("id", OpenApiTypes.STR, OpenApiParameter.PATH,description="A result id to retrieve", required=True),
        ],
        responses={
            status.HTTP_200_OK: SessionSerializer,
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description='Invalid result_id provided'),
            status.HTTP_412_PRECONDITION_FAILED: OpenApiResponse(description='Invalid language'),
        }
    ) 
    def retrieve(self, request, pk=None):
        queryset = Session.objects.all()
        session = get_object_or_404(queryset, result_id=pk)
        serializer = SessionSerializer(session)
        return Response(serializer.data)
    
    @extend_schema(
        request=None,
        description="Update a session after initial creation due to language or version switch",
        parameters=[ 
          OpenApiParameter("result_id", OpenApiTypes.STR, OpenApiParameter.QUERY,description="The result_id to use. Must be a valid reference to a Session object", required=True),
          OpenApiParameter("version_id", OpenApiTypes.INT, OpenApiParameter.QUERY,description="The session version to use. Must be a valid reference to a Session object", required=False),
          OpenApiParameter("lang", OpenApiTypes.STR, OpenApiParameter.QUERY,description="The language code to translate this values", required=False),
        ],
        responses={
            status.HTTP_200_OK: SessionSerializer,
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description='Invalid id or result_id provided'),
            status.HTTP_406_NOT_ACCEPTABLE: OpenApiResponse(description='Invalid version_id provided'),
            status.HTTP_412_PRECONDITION_FAILED: OpenApiResponse(description='Invalid language'),
        }
    ) 
    def partial_update(self, request, pk=None):
        lang = request.query_params.get('lang')
        if lang not in LANGUAGE_CODES:
            return Response(status=status.HTTP_412_PRECONDITION_FAILED) 
        version_id = request.query_params.get('version_id')
        version = None
        if version_id:
            versions = SessionVersion.objects.filter(pk=version_id)
            if versions.count() == 0:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE) 
            else:
                version = versions.first()
        

        
        queryset = Session.objects.all()
        session = get_object_or_404(queryset, pk=pk)
        
        result_id = request.query_params.get('result_id')
        if session.result_id != result_id:
            return Response(status=status.HTTP_404_NOT_FOUND) 
        
        # TODO: This is a side effect. Find something more elegant
        if session.language_code != lang:
            LanguageFeedback.objects.filter(session=session).delete()
        
        session.language_code = lang
        session.version = version
        session.save()

        serializer = SessionSerializer(session)
        return Response(serializer.data)
    
    @extend_schema(
        request=None,
        parameters=[ 
          OpenApiParameter("lang", OpenApiTypes.STR, OpenApiParameter.QUERY,description="The language code to translate this values", required=True),
          OpenApiParameter("result_id", OpenApiTypes.STR, OpenApiParameter.QUERY,description="A result id to copy the results from", required=False),
          OpenApiParameter("user_agent", OpenApiTypes.STR, OpenApiParameter.QUERY,description="An optional user-agent header value for statistics", required=False),
          OpenApiParameter("referrer", OpenApiTypes.STR, OpenApiParameter.QUERY,description="An optional referrer header value for statistics", required=False),
        ],
        responses={
            status.HTTP_200_OK: SessionSerializer,
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description='Invalid result_id provided'),
            status.HTTP_406_NOT_ACCEPTABLE: OpenApiResponse(description='Invalid version_id provided'),
            status.HTTP_412_PRECONDITION_FAILED: OpenApiResponse(description='Invalid language'),
        }
    ) 
    def create(self, request):
        lang = request.query_params.get('lang')
        if lang not in LANGUAGE_CODES:
            return Response(status=status.HTTP_412_PRECONDITION_FAILED)
        
        
        old_result_id= request.query_params.get('result_id')
        referrer= request.query_params.get('referrer')
        user_agent= request.query_params.get('user_agent')

        
        session = self.get_fresh_session(lang, user_agent, referrer)
        old_session = None
        if old_result_id:
            old_sessions = Session.objects.filter(result_id=old_result_id)
            if old_sessions.count() == 0:
                return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                old_session = old_sessions.first()
            if not session.session_origin:
                # copy old meta values
                values = MetaFilterValue.objects.filter(session=old_session) 

                value: MetaFilterValue
                for value in values:
                    value.pk = None
                    value.session = session
                    value.save()


                # copy old selections
                selections = FacetteSelection.objects.filter(session=old_session)
                selection: FacetteSelection
                for selection in selections:
                    # prevent double copies
                    if (
                        FacetteSelection.objects.filter(
                            session=session, facette=selection.facette
                        ).count()
                        == 0
                    ):
                        selection.pk = None
                        selection.session = session
                        selection.save()
                session.session_origin = old_session
                session.save()
        if old_session:
            self.clone_selections(old_session, session)
        serializer = SessionSerializer(session)
        return Response(serializer.data)
    
    def clone_selections(self, old_session: Session, session: Session) -> bool:
        if session.session_origin is not None:
            return False
        selections = FacetteSelection.objects.filter(session=old_session)
        selection: FacetteSelection
        for selection in selections:
            # prevent double copies
            if (
                FacetteSelection.objects.filter(
                    session=session, facette=selection.facette
                ).count()
                == 0
            ):
                selection.pk = None
                selection.session = session
                selection.save()
        session.session_origin = old_session
        session.save()
        return True

    def get_fresh_session(self, language_code: str, user_agent: str, referrer: str) -> Session:
        """
        Create a new session.
        """
        session = Session(user_agent=user_agent)
        session.save()
        session.referrer = referrer
        for group, items in DEFAULT_SESSION_META.items():
            for item in items:
                meta = SessionMeta()
                meta.meta_key = group
                meta.meta_value = item
                meta.session = session
                meta.save()
        session.language_code = language_code
        session.referrer = referrer
        session.save()
        return session
        

