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

from typing import Dict
from django import template

from django.http import HttpRequest

from web.models import Widget, Page, Translateable

from kuusi.settings import KUUSI_URL, KUUSI_NAME, KUUSI_COPYRIGHT_STRING

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


@register.simple_tag(takes_context=True)
def __(context, translatable_object: Translateable, key: str):
    # TODO: LANGUAGE INJECT
    return translatable_object.__(key, language_code="en")

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

@register.inclusion_tag(filename="tags/cookies.html")
def cookies():
    return {}

@register.inclusion_tag(filename="tags/footer.html")
def footer():
    return {
        "left_text": KUUSI_COPYRIGHT_STRING,
        "links": [
            {
                "href": "/about",
                "title": "/about"
            }, 
            {
                "href": "/privacy",
                "title": "/privacy"
            }, 
            {
                "href": "/imprint",
                "title": "/imprint"
            }
        ]
    }