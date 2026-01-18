"""
distrochooser
Copyright (C) 2014-2026 Christoph Müller <mail@chmr.eu>

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

from kuusi.settings import LONG_CACHE_TIMEOUT


def get_translation_haystack(translations: Dict[str, Dict[str, str]], language_code: str) -> Dict[str,str]:
    """
    As the user can provide translations -> use them 
    """
    raw = translations[language_code]
    cache_key = f"translation-{language_code}-feedback"
    cached = cache.get(cache_key)
    approved_provided_feedback = None
    if cached:
        approved_provided_feedback = cached
    else:
        approved_provided_feedback = apps.get_model("web", "LanguageFeedback").objects.filter(is_approved=True).filter(session__language_code=language_code)
        print(approved_provided_feedback)
        cache.set(cache_key, approved_provided_feedback, LONG_CACHE_TIMEOUT)

    
    for element in approved_provided_feedback:
        # As the model LanguageFeedback is not imported, we receive
        # typing errors otherwise.
        # To prevent these, we use # type: ignore here, even as ugly
        key = str(element.language_key) # type: ignore
        value = str(element.value) # type: ignore
        raw[key] = value
    
    return raw