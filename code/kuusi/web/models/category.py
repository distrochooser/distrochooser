"""
distrochooser
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

from typing import Dict
from web.models.http import WebHttpRequest
from web.models import Translateable, TranslateableField, Page
from django.db import models

class Category(Translateable):
    name = TranslateableField(null=False, blank=False, max_length=120)# name AND catalogue id needs to be set, later focused on lranslation
    icon = models.CharField(
        null=False, blank=False, default="bi bi-clipboard2-data", max_length=100
    )
    identifier = models.CharField(null=False, blank=False, max_length=100)
    child_of = models.ForeignKey(
        to="Category",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
        related_name="category_child_of",
    )
    target_page = models.ForeignKey(
        to="Page",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
        related_name="category_target_page",
    )

    def __str__(self) -> str:
        return f"[{self.icon}] {self.name} -> {self.target_page} (child of: {self.child_of})"