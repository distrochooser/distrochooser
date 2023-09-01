"""
kuusi
Copyright (C) 2015-2023  Christoph Müller <mail@chmr.eu>

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

from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseNotAllowed, HttpResponseNotModified

from web.models import TranslationSuggestion
from json import loads

from logging import getLogger
logger = getLogger('root')

def route_add_suggestion(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    body = loads(request.body)
    lang_code = body.get("lang_code")
    dict_values = body.get("dict_values")

    if lang_code is None or dict_values is None or not isinstance(dict_values, dict):
        return HttpResponseNotAllowed(["POST"])
    
    if len(dict_values.keys()) == 0:
        return HttpResponseNotModified()
    
    for key, value in dict_values.items():
        suggestion_matches = TranslationSuggestion.objects.filter(lang_code=lang_code).filter(lang_key=key)
        if suggestion_matches.count() == 1:
            first_match = suggestion_matches.first()
            first_match.amount +=1
            first_match.save()
        else: 
            new_translation = TranslationSuggestion(
                lang_code = lang_code,
                lang_key = key,
                lang_value = value
            )
            new_translation.save()

    return JsonResponse({})