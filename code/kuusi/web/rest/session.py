"""
distrochooser
Copyright (C) 2014-2026 Christoph Müller <distrochooser@chmr.eu>

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

from typing import Dict, Any

from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from kuusi.settings import (
    FRONTEND_URL,
    KUUSI_ICON,
    KUUSI_LOGO,
    KUUSI_NAME,
    RTL_LANGUAGES,
    SESSION_NUMBER_OFFSET,
    IMPRINT,
    PRIVACY,
    DEFAULT_LANGUAGE_CODE,
    ENABLE_TRANSLATION_MODE,
    ENABLE_FEEDBACK_MODE,
    PREVIOUS_VERSION_URL,
    SCORE_MAP,
)
from rest_framework import serializers, status
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet
from web.models import (
    FacetteSelection,
    LanguageFeedback,
    MetaFilterValue,
    Session,
    SessionVersion,
    Violation,
)
from web.util import (
    get_translation_haystack,
    AVAILABLE_LANGUAGES,
    TRANSLATIONS,
    get_translation,
    get_meta_tags,
    is_language_present,
    get_valid_language_code,
)
from django.core.cache import cache
from django.http.response import HttpResponse
from django.utils.timezone import now


class MetaTagsSerializer(serializers.Serializer):
    base_url = serializers.CharField(default=FRONTEND_URL)
    name = serializers.CharField(default=KUUSI_NAME)
    title = serializers.CharField(default=KUUSI_NAME)
    logo = serializers.CharField(default=KUUSI_LOGO)
    meta = serializers.SerializerMethodField()
    icon = serializers.CharField(default=KUUSI_ICON)
    lang = serializers.SerializerMethodField()
    languages = serializers.ListField(default=list(AVAILABLE_LANGUAGES.keys()))

    def get_meta(self, _: None) -> Dict[str, Any]:
        return get_meta_tags(self.context["lang"])

    def get_lang(self, _: None) -> str:
        return get_valid_language_code(self.context["lang"])


class MetaTagViewset(ListModelMixin, GenericViewSet):
    serializer_class = MetaTagsSerializer

    @extend_schema(
        description="Return the list of configured meta tags",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=MetaTagsSerializer,
                description="The list of meta tags available to use",
            ),
        },
        parameters=[
            OpenApiParameter(
                "lang",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description="The language code to translate this values",
                required=False,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        lang = request.query_params.get("lang")
        serializer = MetaTagsSerializer({}, many=False)
        serializer.context["lang"] = lang

        return Response(serializer.data)


class SessionSerializer(serializers.ModelSerializer, MetaTagsSerializer):
    language_codes = serializers.DictField(default=AVAILABLE_LANGUAGES)
    imprint_data = serializers.CharField(default=IMPRINT)
    privacy_data = serializers.CharField(default=PRIVACY)
    default_language = serializers.CharField(default=DEFAULT_LANGUAGE_CODE)
    is_translation_mode_enabled = serializers.BooleanField(
        default=ENABLE_TRANSLATION_MODE
    )
    is_feedback_mode_enabled = serializers.BooleanField(default=ENABLE_FEEDBACK_MODE)
    score_map = serializers.DictField(default=SCORE_MAP)
    previous_version_url = serializers.CharField(default=PREVIOUS_VERSION_URL)

    session_origin = serializers.SerializerMethodField()
    language_values = serializers.SerializerMethodField()
    default_language_values = serializers.SerializerMethodField()
    is_language_rtl = serializers.SerializerMethodField()
    test_count = serializers.SerializerMethodField()
    visitor_count = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = (
            "id",
            "result_id",
            "language_code",
            "default_language",
            "language_codes",
            "session_origin",
            "started",
            "version",
            "base_url",
            "language_values",
            "default_language_values",
            "is_language_rtl",
            "name",
            "logo",
            "meta",
            "icon",
            "test_count",
            "visitor_count",
            "imprint_data",
            "privacy_data",
            "is_translation_mode_enabled",
            "is_feedback_mode_enabled",
            "previous_version_url",
            "imported_from_session",
            "entry_point",
            "score_map",
        )

    def get_session_origin(self, obj: Session) -> str | None:
        return obj.session_origin.result_id if obj.session_origin else None

    def get_meta(self, obj: Session) -> Dict[str, Any]:
        return get_meta_tags(obj.language_code)

    def get_test_count(self, _) -> int:
        # Cache the results for the default amount of time
        # to prevent unwanted database load
        cache_key = f"test-count"
        cached = cache.get(cache_key)
        if cached:
            return cached

        count = SESSION_NUMBER_OFFSET + Session.objects.filter(is_ack=True).count()
        cache.set(cache_key, count)
        return count

    def get_visitor_count(self, _) -> int:
        # Cache the results for the default amount of time
        # to prevent unwanted database load
        cache_key = f"visitor-count"
        cached = cache.get(cache_key)
        if cached:
            return cached
        # The overall visitor count is foggy, as the old sessions are not defined anymore
        # Therefore this is only a rough estimate
        count = SESSION_NUMBER_OFFSET + Session.objects.all().count()
        cache.set(cache_key, count)
        return count

    def get_is_language_rtl(self, obj: Session) -> bool:
        return obj.is_rtl

    def get_language_values(self, obj: Session) -> Dict[str, str]:
        return get_translation_haystack(TRANSLATIONS, obj.language_code)

    def get_default_language_values(self, obj: Session) -> Dict[str, str]:
        return get_translation_haystack(TRANSLATIONS, DEFAULT_LANGUAGE_CODE)


class SessionVersionSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()

    class Meta:
        model = SessionVersion
        fields = "__all__"

    def get_text(self, obj: SessionVersion) -> str:
        session: Session = self.context["session"]
        return get_translation(f"{obj.description}-description", session.language_code)


class SessionViewSet(ViewSet):
    serializer_class = Session
    queryset = Session.objects.all()

    @extend_schema(
        request=None,
        parameters=[
            OpenApiParameter(
                "id",
                OpenApiTypes.STR,
                OpenApiParameter.PATH,
                description="A result id to retrieve",
                required=True,
            ),
        ],
        responses={
            status.HTTP_200_OK: SessionSerializer,
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Invalid result_id provided"
            ),
        },
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
            OpenApiParameter(
                "result_id",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description="The result_id to use. Must be a valid reference to a Session object",
                required=True,
            ),
            OpenApiParameter(
                "version_id",
                OpenApiTypes.INT,
                OpenApiParameter.QUERY,
                description="The session version to use. Must be a valid reference to a Session object",
                required=False,
            ),
            OpenApiParameter(
                "lang",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description="The language code to translate this values",
                required=False,
            ),
            OpenApiParameter(
                "is_container_visible",
                OpenApiTypes.BOOL,
                OpenApiParameter.QUERY,
                description="The language code to translate this values",
                required=False,
                default=False,
            ),
        ],
        responses={
            status.HTTP_200_OK: SessionSerializer,
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Invalid id or result_id provided"
            ),
            status.HTTP_406_NOT_ACCEPTABLE: OpenApiResponse(
                description="Invalid version_id provided"
            ),
        },
    )
    def partial_update(self, request, pk=None):
        lang = get_valid_language_code(request.query_params.get("lang"))
        version_id = request.query_params.get("version_id")
        version: SessionVersion | None = None
        if version_id:
            versions = SessionVersion.objects.filter(pk=version_id)
            if versions.first() is None:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                version = versions[0]

        container_update_needed = (
            request.query_params.get("is_container_visible", "") != ""
        )
        is_container_visible: bool = (
            request.query_params.get("is_container_visible", "") == "true"
        )
        sessions = Session.objects.filter(pk=pk)

        session = sessions.first()
        if not session:
            return Response(status=status.HTTP_404_NOT_FOUND)

        result_id = request.query_params.get("result_id")
        if session.result_id != result_id:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # TODO: This is a side effect. Find something more elegant
        if session.language_code != lang:
            LanguageFeedback.objects.filter(session=session).delete()

        if container_update_needed:
            session.is_container_visible = is_container_visible

        session.language_code = lang
        # TODO: Fix typing warning
        # Error complains about version not being able to be set, which should not be the case
        session.version = version  # type: ignore
        session.save()

        serializer = SessionSerializer(session)
        return Response(serializer.data)

    @extend_schema(
        request=None,
        parameters=[
            OpenApiParameter(
                "lang",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description="The language code to translate this values",
                required=True,
            ),
            OpenApiParameter(
                "result_id",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description="A result id to copy the results from",
                required=False,
            ),
            OpenApiParameter(
                "user_agent",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description="An optional user-agent header value for statistics",
                required=False,
            ),
            OpenApiParameter(
                "referrer",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description="An optional referrer header value for statistics",
                required=False,
            ),
            OpenApiParameter(
                name="entry_point",
                location=OpenApiParameter.QUERY,
                description="See EntryPointChoice",
                required=True,
                type=OpenApiTypes.STR,
                enum=Session.EntryPointChoice,
            ),
        ],
        responses={
            status.HTTP_200_OK: SessionSerializer,
            status.HTTP_406_NOT_ACCEPTABLE: OpenApiResponse(
                description="Invalid version_id provided"
            ),
            status.HTTP_509_BANDWIDTH_LIMIT_EXCEEDED: OpenApiResponse(
                description="Timeout"
            ),
        },
    )
    def create(self, request):
        lang = get_valid_language_code(request.query_params.get("lang"))
        old_result_id = request.query_params.get("result_id")
        referrer = request.query_params.get("referrer")
        user_agent = request.query_params.get("user_agent")
        entry_point = request.query_params.get("entry_point")

        # As the session endpoint is _the_ central endpoint -> use for blocking
        # See ADR-0036 for details
        violations = Violation.objects.filter(user_agent=user_agent, invalidated=False)
        if violations.count() > 0:
            violation = violations.first()
            violation.hits += 1
            violation.last_hit = now()
            if violation.valid_until and violation.valid_until < now().date():
                violation.invalidated = True
            violation.save()
            text = violation.reason
            if violation.valid_until:
                text += f" Block will be lifted: {violation.valid_until}"
            return HttpResponse(
                status=status.HTTP_509_BANDWIDTH_LIMIT_EXCEEDED, content=text
            )

        session = self.get_fresh_session(lang, user_agent, referrer, entry_point)
        old_session = None
        if old_result_id:
            old_session = Session.get(old_result_id)
            if old_session and not session.session_origin:
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
                        selection.imported_from_answer = None
                        selection.save()
                # TODO: Find reason for typing error
                # Find way to remove # type: ignore
                session.imported_from_session = None
                session.session_origin = old_session  # type: ignore
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
        # TODO: Find reason for typing error
        # Find way to remove # type: ignore
        session.session_origin = old_session  # type: ignore
        session.save()
        return True

    def get_fresh_session(
        self, language_code: str, user_agent: str, referrer: str, entry_point: str
    ) -> Session:
        """
        Create a new session.
        """
        session = Session()
        session.user_agent = user_agent
        session.referrer = referrer
        session.language_code = language_code
        session.referrer = referrer
        session.entry_point = entry_point
        session.save()
        return session
