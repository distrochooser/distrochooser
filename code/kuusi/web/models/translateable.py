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

from __future__ import annotations

from typing import Any

from django.db import models
from django.db.models.signals import pre_delete
from django.db.backends.signals import connection_created
from django.dispatch import receiver
from logging import getLogger
from os.path import join, exists
from json import loads, dumps
from os import mkdir, listdir

logger = getLogger("root")

from kuusi.settings import (
    LOCALE_PATHS,
    LANGUAGE_CODES
)

TRANSLATIONS = {}


def hot_load_translations(**kwargs):
    path = join(LOCALE_PATHS[0])
    files = listdir(path)
    for file in files:
        if ".json" in file:
            parts = file.split("-")
            language = parts[1].replace(".json", "").lower()
            if language not in TRANSLATIONS:
                TRANSLATIONS[language] = {}
            full_path = join(path, file)
            content = loads(open(full_path, "r").read())
            for key, value in content.items():
                TRANSLATIONS[language][key] = value
            print(f"Finished reading file {full_path} for translation. Language = {language}")
# Do this once in the livetime of the instance
# TODO: Move me to a better place!
hot_load_translations()


class TranslateableField(models.CharField):
    "A field which can be translated"

    def __init__(self, *args, **kwargs):
        kwargs["help_text"] = "A comment for translators to identify this value"
        super().__init__(*args, **kwargs)

    def get_msg_id(self, model_instance: Translateable):
        """
        Get a unique identifier to be used for translation purposes.
        """
        identifier = model_instance.catalogue_id
        return f"{identifier}-{self.name}"

    def pre_save(self, model_instance: Translateable, add: bool) -> Any:
        """
        Update records to make sure there is a record existing at all the time
        """
        if len(LOCALE_PATHS) == 0:
            raise Exception(f"No locale paths are set")
        model_type = type(model_instance).__name__
        msg_id = self.get_msg_id(model_instance)
        # Make sure that the TranslateAbleField has a record we can reference
        TranslateableFieldRecord.objects.filter(
            msg_id=msg_id,
            model_type=model_type
        ).delete()
        TranslateableFieldRecord.objects.create(
            msg_id=msg_id,
            model_type=model_type
        )
        self.update_json(model_type, msg_id)
        return super().pre_save(model_instance, add)

    def update_json(self, model_type: str, msg_id: str):
        for locale in LANGUAGE_CODES:
            lowercase_locale = locale.lower()
            lowercase_model_type =model_type.lower()
            path = join(LOCALE_PATHS[0], f"{lowercase_model_type}-{lowercase_locale}.json")
            entries = {}
            if exists(path):
                with open(path, "r") as file:
                    entries = loads(file.read())
            if msg_id not in entries:
                entries[msg_id] = None
            with open(path, "w") as file:
                file.write(dumps(entries))



class TranslateableFieldRecord(models.Model):
    msg_id = models.CharField(null=False, blank=False, max_length=250)
    model_type = models.TextField(null=True, blank=True, max_length=200)
    def __str__(self) -> str:
        return self.msg_id


class Translateable(models.Model):
    """
    This class is just used to trigger a signal, which clears up unused TranslateableFieldRecords

    If a TranslateField shall be used, the model must inherit this class.
    """
    # The catalogue_id needs to be set to allow uniquely identify the translated fields using this
    catalogue_id = models.CharField(null=True, blank=True, default=None, max_length=255) 

    is_invalidated = models.BooleanField(default=False)
    invalidation_id = models.CharField(max_length=255, default=None,null=True,blank=True)

    def __str__(self) -> str:
        return f"[{self.invalidation_id}] ({self.catalogue_id})"
    def get_msgd_id_of_field(self, key: str) -> str:
        return self._meta.get_field(key).get_msg_id(self)
    def __(self, key: str, language_code: str = "en") -> str:
        msg_id = self.get_msgd_id_of_field(key)
        return f"{TRANSLATIONS[language_code][msg_id]}" if language_code in TRANSLATIONS and msg_id in TRANSLATIONS[language_code] and TRANSLATIONS[language_code][msg_id] is not None  else msg_id
     

    def remove_translation_records(self):
        """
        Removes the translation records form the database.
        """
        fields = self._meta.get_fields()

        field: models.Field | TranslateableField
        for field in fields:

            if isinstance(field, TranslateableField):
                TranslateableFieldRecord.objects.filter(
                    msg_id=field.get_msg_id(self)
                ).delete()

@receiver(pre_delete, sender=Translateable)
def translateable_removing(sender, instance, using, **kwargs):
    origin: Translateable | models.QuerySet = kwargs["origin"]
    if isinstance(origin, models.QuerySet):
        entry: Translateable
        for entry in origin:
            entry.remove_translation_records()
    else:
        origin.remove_translation_records()
