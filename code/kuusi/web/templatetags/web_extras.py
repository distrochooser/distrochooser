"""
kuusi
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

from typing import Dict, List
from django import template

from django.utils.translation import gettext as _
from django.utils import safestring
from django.utils.html import strip_tags
from django.http import HttpRequest
from django.forms import Form, Field, ValidationError
from django.forms.utils import ErrorDict

from web.models import SessionMeta, Widget, Page, FacetteSelection, WebHttpRequest, Translateable, Choosable, FacetteAssignment, ChoosableMeta, Session
from web.models import TRANSLATIONS, RTL_TRANSLATIONS
from web.forms import WarningForm
from kuusi.settings import KUUSI_COPYRIGHT_STRING, KUUSI_INFO_STRING, LANGUAGE_CODES, KUUSI_META_TAGS, DEFAULT_LANGUAGE_CODE, LOCALE_MAPPING

import logging

logger = logging.getLogger(__name__)

register = template.Library()


def _i18n_get_value(language_code: str, translateable_object: Translateable | safestring.SafeString | str, key: str = None):
    value = None
    needle = None
    default_value =  None
    if language_code == "favicon":
        return {"value": "", "needle": needle, "is_missing": True}
    if not str:
        raise Exception("Key is required")
    if isinstance(translateable_object, Translateable):
        needle = key
        value =  translateable_object.__(key, language_code=language_code)
        default_value =  translateable_object.__(key, language_code=DEFAULT_LANGUAGE_CODE)
    else:
        needle = str(translateable_object)
        default_value = TRANSLATIONS["en"][needle]  if needle in TRANSLATIONS["en"] and TRANSLATIONS["en"][needle] is not None else needle
        value = TRANSLATIONS[language_code][needle] if needle in TRANSLATIONS[language_code] and TRANSLATIONS[language_code][needle] is not None else needle
    is_missing = language_code != "en" and default_value == value
    return {"value": value, "needle": needle, "is_missing": is_missing}


@register.simple_tag
def _i18n_(language_code: str, translateable_object: Translateable | safestring.SafeString | str, key: str = None):
    got =  _i18n_get_value(language_code, translateable_object,key)
    return got["value"]
