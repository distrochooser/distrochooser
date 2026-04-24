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

from __future__ import annotations

from typing import Any, Dict
from django.apps import apps
from django.core.cache import cache
from os.path import join, exists

from kuusi.settings import LONG_CACHE_TIMEOUT
from json import loads, dumps


from kuusi.settings import (
    LOCALE_PATHS,
    ENABLE_TRANSLATION_MODE 
)
from os import listdir

def get_translation_haystack(translations: Dict[str, Dict[str, str]], language_code: str) -> Dict[str,str]:
    """
    As the user can provide translations -> use them 
    """
    raw = translations[language_code]
    if not ENABLE_TRANSLATION_MODE:
        return raw
    cache_key = f"translation-{language_code}-feedback"
    cached = cache.get(cache_key)
    approved_provided_feedback = None
    if cached:
        approved_provided_feedback = cached
    else:
        approved_provided_feedback = apps.get_model("web", "LanguageFeedback").objects.filter(is_approved=True).filter(session__language_code=language_code)
        cache.set(cache_key, approved_provided_feedback, LONG_CACHE_TIMEOUT)

    
    for element in approved_provided_feedback:
        # As the model LanguageFeedback is not imported, we receive
        # typing errors otherwise.
        # To prevent these, we use # type: ignore here, even as ugly
        key = str(element.language_key) # type: ignore
        value = str(element.value) # type: ignore
        raw[key] = value
    
    return raw


TRANSLATIONS = {}

def hot_load_translations(**kwargs):
    path = join(LOCALE_PATHS[0])
    files = listdir(path)
    for file in files:
        if ".json" in file:
            parts = file.split("-")
            language = parts[1].replace(".json", "").lower()
            if language not in TRANSLATIONS:
                TRANSLATIONS[language] = {}
            full_path = join(path, file)
            content = loads(open(full_path, "r").read())
            for key, value in content.items():
                TRANSLATIONS[language][key] = value

def get_translation(key: str | None, language_code: str) -> str:
    if not key:
        return "no-translation"
    if language_code not in TRANSLATIONS:
        return key
    
    if key not in TRANSLATIONS[language_code]:
        return key
    
    return TRANSLATIONS[language_code][key]