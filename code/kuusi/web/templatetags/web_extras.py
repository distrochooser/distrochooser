"""
kuusi
Copyright (C) 2014-2023  Christoph Müller <mail@chmr.eu>

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
from django.utils.translation import get_language
from django.utils import safestring
from django.http import HttpRequest
from django.forms import Form, Field, ValidationError
from django.forms.utils import ErrorDict

from web.models import Widget, Page, FacetteSelection, WebHttpRequest, Translateable, Choosable, FacetteAssignment, ChoosableMeta, TranslationSuggestion

from kuusi.settings import KUUSI_COPYRIGHT_STRING, KUUSI_INFO_STRING, LANGUAGE_CODES

register = template.Library()

@register.filter
def prev(haystack: Dict, index: int):
    if index == 0:
        return None

    return list(haystack.keys())[index - 1]


@register.simple_tag(takes_context=True)
def render_widget(context, widget: Widget, page: Page):
    """
    Triggers render() on a given Widget while injecting the global request context into the call.
    """
    request: HttpRequest = context["request"]
    return widget.render(request, page)


@register.inclusion_tag(takes_context=True, filename="tags/i18n.html")
def _i18n(context, translateable_object: Translateable | safestring.SafeString | str, key: str = None):
    language_code = get_language()
    value = None
    needle = None
    if not str:
        raise Exception("Key is required")
    if translateable_object and not key and isinstance(translateable_object, safestring.SafeString):
        needle = str(translateable_object)
        value =  _(translateable_object) # If they translateable_object is a safestring, use Django's translation
    elif isinstance(translateable_object, str):
        needle = translateable_object
        value =  _(translateable_object)
    else:
        value =  translateable_object.__(key, language_code=language_code)
        needle = key
    # TODO: Show suggestions
    suggestions = list(TranslationSuggestion.objects.filter(lang_code=language_code).filter(lang_key=needle).values_list("lang_value",flat=True))
    
    return {"value": value, "needle": needle, "suggestions": suggestions }

@register.inclusion_tag(filename="tags/page.html", takes_context=True)
def page(context, page: Page):
    request: HttpRequest = context["request"]
    return {"page": page, "request": request}


@register.inclusion_tag(filename="tags/logo.html")
def logo():
    return {}


@register.inclusion_tag(filename="tags/step.html", takes_context=True)
def step(context, step: Dict):
    return step

@register.inclusion_tag(filename="tags/step_content.html")
def step_content(step: Dict):
    return {"step": step}


@register.inclusion_tag(filename="tags/cookies.html")
def cookies():
    return {}


@register.inclusion_tag(filename="tags/footer.html", takes_context=True)
def footer(context):
    request: HttpRequest = context["request"]
    return {
        "language_code": request.LANGUAGE_CODE,
        "left_text": KUUSI_COPYRIGHT_STRING,
        "free_nav": KUUSI_INFO_STRING
    }


@register.inclusion_tag(filename="tags/sub_facettes.html", takes_context=True)
def sub_facettes(context, form: Form, current_facette: str, weights: Dict):
    request: WebHttpRequest = context["request"]
    session = request.session_obj
    child_fields = []
    parent = form.fields.get(current_facette)
    is_selected = (
        FacetteSelection.objects.filter(facette__catalogue_id=current_facette, session=session).count() > 0
    )
    for field_name in form.fields:
        field = form.fields.get(field_name)
        parent_identifier = field.widget.attrs.get("data-ku-parent")
        is_child = parent_identifier == current_facette
        if is_child:
            child_fields.append(field_name)

    has_facettes = child_fields.__len__() > 0
    return {
        "is_selected": is_selected,
        "current_facette": current_facette,
        "parent": parent,
        "has_facettes": has_facettes,
        "child_fields": child_fields,
        "form": form,
        "weights": weights
    }



@register.inclusion_tag(filename="tags/choosable.html")
def choosable(result: Dict):
    choosable: Choosable = result.get("choosable")
    score: float = result.get("score")
    assignments: List[FacetteAssignment] = result.get("assignments")
    return {"choosable": choosable, "score": score, "assignments": assignments}


@register.inclusion_tag(filename="tags/meta_value.html")
def meta_value(obj: ChoosableMeta):
    return {"obj": obj}

@register.inclusion_tag(filename="tags/weight.html")
def weight(field: Field, weights: Dict):
    value = 0
    if field.name in weights:
        value = weights.get(field.name)
    return {"field": field, "value": value}

def flatten_errors_warnings(haystack: ErrorDict):
    """
    Returns a "flattened" dict containing the error messages for human display
    """
    result: Dict = {}
    for key, errors in haystack.as_data().items():
        for error in errors:
            message = str(error.message)
            matched = False
            for result_key, result_value in result.items():
                if result_key != key:
                    if result_value == message:
                        old_key = result_key
                        new_key = old_key + "," + key
                        del result[old_key]
                        result[new_key] = message
                        matched = True
                        break
            
            if not matched:
                result[key] = message
                
    return result

@register.inclusion_tag(filename="tags/errors.html")
def errors(errors: Dict[str, List[ValidationError]]):
    # TODO: Make less redundant with warnings()
    return {"haystack": flatten_errors_warnings(errors), "severity": "danger"}


@register.inclusion_tag(filename="tags/errors.html")
def warnings(warnings: Dict[str, List[ValidationError]]):
    # FIXME: warnings should be using the same structure as errors() first parameter, but it doesnt. 
    return {}
    return {"haystack": flatten_errors_warnings(warnings), "severity": "warning"}


@register.inclusion_tag(filename="tags/language_select.html")
def language_select():
    return {"language_codes": LANGUAGE_CODES}