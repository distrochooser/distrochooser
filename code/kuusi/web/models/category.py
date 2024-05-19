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

from typing import Dict
from web.models.http import WebHttpRequest
from web.models import Translateable, TranslateableField, Session, Page
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

    def to_step(
        self,
        request: WebHttpRequest, 
        is_last: bool = False,
    ) -> Dict | None:
        """
        Returns the structure so that the custom tag "steps" can generate the navigation element.

        If the target page is not fitting the version of the session, None is returned.
        """
        language_code = request.LANGUAGE_CODE
        session = request.session_obj

        target = None
        target_page: Page = self.target_page
        is_error = False
        is_warning = False
        is_marked = False
        is_active = False

        if target_page:
            target = target_page.href

            if not target_page.is_visible(session):
                return None
            is_answered = target_page.is_answered(session)
            is_marked = target_page.is_marked(session)
            is_warning = target_page.is_warning(session)
            is_error = target_page.is_error(session)
            is_active = target_page.is_active(request)

        return {
            "title": self.__("name", language_code),
            "href": target,
            "active": is_active,
            "answered": is_answered,
            "marked": is_marked,
            "warning": is_warning,
            "error": is_error,
            "last": is_last,
        }

    def __str__(self) -> str:
        return f"[{self.icon}] {self.name} -> {self.target_page} (child of: {self.child_of})"