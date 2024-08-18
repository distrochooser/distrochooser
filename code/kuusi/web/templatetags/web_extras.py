"""
kuusi
Copyright (C) 2014-2024  Christoph Müller  <mail@chmr.eu>

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

from web.models import SessionMeta, Widget, Page, FacetteSelection, WebHttpRequest, Translateable, Choosable, FacetteAssignment, ChoosableMeta
from web.models import TRANSLATIONS, RTL_TRANSLATIONS
from web.models.sessionversion import A11Y_OPTIONS_BODYCLASSES
from web.forms import WarningForm
from kuusi.settings import KUUSI_COPYRIGHT_STRING, KUUSI_INFO_STRING, LANGUAGE_CODES, KUUSI_META_TAGS, DEFAULT_LANGUAGE_CODE

register = template.Library()

@register.filter
def prev(haystack: Dict, index: int):
    if index == 0:
        return None

    return list(haystack.keys())[index - 1]

@register.filter
def weight_abs(raw):
    return abs(raw)

@register.filter
def replace_weight_signs(raw):
    return str(abs(raw)).replace('.', '-')

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.simple_tag(takes_context=True)
def render_widget(context, widget: Widget, page: Page):
    """
    Triggers render() on a given Widget while injecting the global request context into the call.
    """
    request: HttpRequest = context["request"]
    return widget.render(request, page)

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

@register.inclusion_tag(filename="tags/i18n.html")
def _i18n_(language_code: str, translateable_object: Translateable | safestring.SafeString | str, key: str = None):
    got =  _i18n_get_value(language_code, translateable_object,key)
    return got

@register.inclusion_tag(filename="tags/page.html", takes_context=True)
def page(context, page: Page):
    request: HttpRequest = context["request"]
    session = request.session_obj
    return {"page": page, "request": request, "session": session}


@register.inclusion_tag(filename="tags/logo.html")
def logo(language_code: str, on_static_page: bool = False):
    return {"on_static_page": on_static_page, "is_rtl": language_code in RTL_TRANSLATIONS}


@register.inclusion_tag(filename="tags/step.html")
def step(language_code: str, step: Dict):
    step["language_code"] = language_code
    return step

@register.inclusion_tag(filename="tags/step_content.html")
def step_content(language_code: str, step: Dict):
    return {"language_code": language_code, "step": step}

@register.inclusion_tag(filename="tags/step_markings.html")
def step_markings(language_code: str, step: Dict):
    return {"language_code": language_code, "step": step}


@register.inclusion_tag(filename="tags/cookies.html", takes_context=True)
def cookies(context):
    request: HttpRequest = context["request"]
    return {
        "language_code": request.LANGUAGE_CODE
    }


@register.inclusion_tag(filename="tags/footer.html")
def footer(language_code: str):
    return {
        "language_code": language_code,
        "left_text": KUUSI_COPYRIGHT_STRING,
        "free_nav": KUUSI_INFO_STRING,
        "is_rtl": language_code in RTL_TRANSLATIONS
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
def choosable(language_code: str, result: Dict):
    choosable: Choosable = result.get("choosable")
    score: float = result.get("score")
    assignments: List[FacetteAssignment] = result.get("assignments")
    return {"choosable": choosable, "language_code": language_code, "score": score, "assignments": assignments}


@register.inclusion_tag(filename="tags/meta_value.html")
def meta_value(obj: ChoosableMeta):
    return {"obj": obj, "choosable": obj.meta_choosable}

@register.inclusion_tag(filename="tags/weight.html")
def weight(language_code: str, field: Field, weights: Dict):
    value = 0
    if field.name in weights:
        value = weights.get(field.name)
    return {"language_code": language_code, "field": field, "value": value}

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
def errors(language_code: str, form: WarningForm):
    errors: Dict[str, List[ValidationError]] = form.behaviour_errors
    warnings: Dict[str, List[ValidationError]] = form.behaviour_warnings
    information: Dict[str, List[ValidationError]] = form.behaviour_information
    return {"language_code": language_code, "errors": errors, "warnings": warnings, "information": information}

@register.inclusion_tag(filename="tags/errors_inner.html")
def errors_inner(language_code: str, criticality: str, haystack: Dict[str, List[str]], title: str):
    return {"language_code": language_code, "criticality": criticality, "haystack": haystack, "title": title}


@register.inclusion_tag(takes_context=True,filename="tags/language_select.html")
def language_select(context):
    request: WebHttpRequest = context["request"]
    session_result_id = request.session_obj.result_id
    language_code = request.session_obj.language_code
    return {"result_id": session_result_id, "language_codes": LANGUAGE_CODES, "language_code": language_code, "get_params": request.GET.urlencode()}

@register.simple_tag()
def rtl_class(language_code: str):
    return "ku-rtl" if  language_code in RTL_TRANSLATIONS else "ku-ltr"

@register.inclusion_tag(filename="tags/meta_tags.html")
def meta_tags(language_code:str):
    result = KUUSI_META_TAGS
    for key, _ in result.items():
        if "description" in key:
            result[key] = strip_tags(TRANSLATIONS[language_code]["DESCRIPTION_TEXT"])
    return {
        "tags": result
    }

@register.inclusion_tag(filename="tags/feedback_state.html")
def feedback_state(language_code: str, assignment: FacetteAssignment, choosable: Choosable):
    is_flagged = assignment.is_flagged(choosable)

    title = _i18n_get_value(language_code, "FLAG_THIS_ASSIGNMENT" if not is_flagged else "REMOVE_FLAG_ASSIGNMENT")["value"]
    return {"title": title, "assignment": assignment, "choosable": "choosable", "is_flagged": is_flagged}


@register.simple_tag(takes_context=True)
def a11y_classes(context):
    request: HttpRequest = context["request"]
    #static pages might not feature that session_obj -> return empty string
    if not hasattr(request, "session_obj"):
        return ""
    session = request.session_obj
    session_metas = SessionMeta.objects.filter(session=session)
    class_string = ""

    meta: SessionMeta
    for meta in session_metas:
        if meta.meta_key in A11Y_OPTIONS_BODYCLASSES:
            class_string += " " + A11Y_OPTIONS_BODYCLASSES[meta.meta_key]
        # The font size is digged into the meta_value -> check for these aswell
        if meta.meta_value in A11Y_OPTIONS_BODYCLASSES:
            class_string += " " + A11Y_OPTIONS_BODYCLASSES[meta.meta_value]

    return class_string


@register.inclusion_tag(filename="tags/next_item.html")
def next_item(next_item: str | None):
    return {"next_item": next_item}

@register.inclusion_tag(filename="tags/previous_item.html")
def previous_item(previous_item: str | None):
    return {"previous_item": previous_item}