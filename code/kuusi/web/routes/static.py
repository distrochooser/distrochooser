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


from web.models import Session, WebHttpRequest
from django.http import (
    HttpResponse
)
from django.template import loader
from django.utils.translation import gettext_lazy as _
from django.utils import translation
from os.path import join

from kuusi.settings import (
    SESSION_NUMBER_OFFSET
)
from kuusi.legal import LEGAL_TEXT, LEGAL_TEXT_DISCLAIMER
from web.models import Session, WebHttpRequest
from web.helper import forward_helper
from logging import getLogger

def route_about(request: WebHttpRequest, language_code: str = None):
    template = loader.get_template("about.html")
    context = {
        "count": SESSION_NUMBER_OFFSET  + Session.objects.all().count()
    }
    return HttpResponse(template.render(context, request))


def route_privacy(request: WebHttpRequest, language_code: str = None):
    template = loader.get_template("privacy.html")
    context = {}
    return HttpResponse(template.render(context, request))


def route_contact(request: WebHttpRequest, language_code: str = None):
    template = loader.get_template("contact.html")
    context = {
        "text": LEGAL_TEXT,
        "disclaimer_text": LEGAL_TEXT_DISCLAIMER
    }
    return HttpResponse(template.render(context, request))