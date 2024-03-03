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

from web.models import Widget, Page
from os.path import join
from os import listdir
from django.db import models
from kuusi.settings import BASE_DIR
from django import forms
from django.http import HttpRequest
from django.template import loader

class HTMLWidget(Widget):
    template = models.CharField(null=False, blank=False, max_length=25)

    def __init__(self, *args, **kwargs):
        template_path = join(BASE_DIR, "web", "templates", "widgets")
        raw_templates = listdir(template_path)
        templates = []
        for template in raw_templates:
            templates.append((template, template))
        self._meta.get_field("template").choices = templates
        self._meta.get_field("template").widget = forms.Select(choices=templates)
        super(HTMLWidget, self).__init__(*args, **kwargs)

    def __str__(self) -> str:
        return self.template

    def render(self, request: HttpRequest, page: Page):
        render_template = loader.get_template(f"widgets/{self.template}")
        return render_template.render({}, request)

    def proceed(self, request: HttpRequest, page: Page) -> bool:
        return True