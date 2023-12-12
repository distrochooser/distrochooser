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

from typing import Dict
from django.db import models
from web.models import Translateable, TranslateableField

class Choosable(Translateable):
    """
    Element ot be choosed.

    Must be translated
    """

    name = TranslateableField(null=False, blank=False, max_length=120)
    description = TranslateableField(
        null=True, blank=True, default=None, max_length=120
    )

    def __str__(self) -> str:
        return f"{self.name}"

    @property
    def meta(self) -> Dict[str, any]:
        meta_objects = ChoosableMeta.objects.filter(meta_choosable=self).order_by(
            "meta_name"
        )
        result = {}
        meta_objects: ChoosableMeta
        for meta_object in meta_objects:
            result[meta_object.meta_name] = meta_object

        return result


class ChoosableMeta(Translateable):
    meta_choosable = models.ForeignKey(
        to=Choosable,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="choosablemeta_choosable",
    )

    class MetaType(models.TextChoices):
        TEXT = "TEXT", "TEXT"
        FLAG = "FLAG", "FLAG"
        LINK = "LINK", "LINK"
        DATE = "DATE", "DATE"

    class MetaName(models.TextChoices):
        CREATED = "CREATED", "CREATED"
        COUNTRY = "COUNTRY", "COUNTRY"
        LICENSES = "LICENSES", "LICENSES"
        WEBSITE = "WEBSITE", "WEBSITE"

    meta_type = models.CharField(
        max_length=20, choices=MetaType.choices, default=MetaType.TEXT
    )
    meta_title = TranslateableField(null=True, blank=True, max_length=120)
    meta_name = models.CharField(
        max_length=25,
        blank=False,
        null=False,
        choices=MetaName.choices,
        default=MetaName.CREATED,
    )
    meta_value = models.CharField(
        max_length=255, blank=False, null=False, default="A value"
    )

    def __str__(self) -> str:
        return f"{self.meta_choosable}: {self.meta_name} ({self.meta_type}) -> {self.meta_value}"
