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
from django.dispatch import receiver
from logging import getLogger
from os.path import join, exists
from polib import pofile
from os import mkdir

logger = getLogger("root")

from kuusi.settings import (
    LOCALE_PATHS,
    LANGUAGES
)
class TranslateableField(models.CharField):
    "A field which can be translated"

    def __init__(self, *args, **kwargs):
        kwargs["help_text"] = "A comment for translators to identify this value"
        super().__init__(*args, **kwargs)

    def get_msg_id(self, model_instance: Translateable):
        """
        Get a unique identifier to be used for translation purposes.
        """
        model_type = type(model_instance).__name__
        identifier = model_instance.pk
        if model_instance.catalogue_id:
            identifier = model_instance.catalogue_id
        return f"{model_type}_{identifier}_{self.name}".upper()

    def get_po_block(self, model_instance: Translateable):
        """
        Return the block to be written into the PO file.
        A msg_str might be appended if an translation is existing within the locale context.
        """
        comment = self.value_from_object(model_instance)
        name = self.name
        model_type = type(model_instance).__name__
        pk = model_instance.pk
        msg_id = self.get_msg_id(model_instance)
        return f'\n# Model reference: {model_type}.{pk}\n# Attribute name: {name}, remark: {comment}\nmsgid "{msg_id}"'

    def pre_save(self, model_instance: Translateable, add: bool) -> Any:
        """
        Update records to make sure there is a record existing at all the time
        """
        if len(LOCALE_PATHS) == 0:
            raise Exception(f"No locale paths are set")

        # Make sure that the TranslateAbleField has a record we can reference
        TranslateableFieldRecord.objects.filter(
            msg_id=self.get_msg_id(model_instance)
        ).delete()
        record = TranslateableFieldRecord.objects.create(
            msg_id=self.get_msg_id(model_instance),
            po_block=self.get_po_block(model_instance),
        )

        logger.debug(f"TranslatableFieldRecord is {record}")
        model_instance.update_po_file()
        return super().pre_save(model_instance, add)


class TranslateableFieldRecord(models.Model):
    msg_id = models.CharField(null=False, blank=False, max_length=250)
    po_block = models.TextField(null=True, blank=True, max_length=1000)

    def __str__(self) -> str:
        return self.msg_id


class Translateable(models.Model):
    """
    This class is just used to trigger a signal, which clears up unused TranslateableFieldRecords

    If a TranslateField shall be used, the model must inherit this class.
    """

    catalogue_id = models.CharField(null=True, blank=True, default=None, max_length=255)

    is_invalidated = models.BooleanField(default=False)
    invalidation_id = models.CharField(max_length=255, default=None,null=True,blank=True)

    def __str__(self) -> str:
        return f"[{self.invalidation_id}] ({self.catalogue_id})"

    def __(self, key: str, language_code: str = "en") -> str:
        msg_id = self._meta.get_field(key).get_msg_id(self)
        # TODO: make this block in a function
        # TODO: make this in memory
        translation_path = join(
            LOCALE_PATHS[0], language_code, "LC_MESSAGES", "translateable.po"
        )
        existing_record_translations = {}
        if exists(translation_path):
            po = pofile(translation_path)
            for entry in po:
                existing_record_translations[entry.msgid] = entry.msgstr
        if (
            msg_id not in existing_record_translations
            or len(existing_record_translations[msg_id]) == 0
        ):
            return msg_id
        return existing_record_translations[msg_id]

    def remove_translation_records(self):
        """
        Removes the translation records form the database.
        """
        fields = self._meta.get_fields()

        field: models.Field | TranslateableField
        for field in fields:
            field_type = type(field)
            field_name = field.name
            if isinstance(field, TranslateableField):
                logger.debug(f"Removing field records for {self}:{field_type} ({field_name})")
                TranslateableFieldRecord.objects.filter(
                    msg_id=field.get_msg_id(self)
                ).delete()

    def update_po_file(self):
        """
        Update the PO file to represent the currently used records
        """
        for lang in LANGUAGES:
            key = lang[0]
            if not exists(join(LOCALE_PATHS[0], key)):
                mkdir(join(LOCALE_PATHS[0], key))
            if not exists(join(LOCALE_PATHS[0], key, "LC_MESSAGES")):
                mkdir(join(LOCALE_PATHS[0], key, "LC_MESSAGES"))

            translation_path = join(
                LOCALE_PATHS[0], key, "LC_MESSAGES", "translateable.po"
            )
            existing_record_translations = {}
            if exists(translation_path):
                po = pofile(translation_path)
                for entry in po:
                    existing_record_translations[entry.msgid] = entry.msgstr

            # write the PO file
            all_records = TranslateableFieldRecord.objects.all().order_by("-msg_id")
            with open(translation_path, "w") as file:
                record: TranslateableFieldRecord
                for record in all_records:
                    msg_str = ""
                    if record.msg_id in existing_record_translations:
                        msg_str = existing_record_translations[record.msg_id]
                    file.write(record.po_block + f'\nmsgstr "{msg_str}"')


@receiver(pre_delete, sender=Translateable)
def translateable_removing(sender, instance, using, **kwargs):
    origin: Translateable | models.QuerySet = kwargs["origin"]
    if isinstance(origin, models.QuerySet):
        entry: Translateable
        for entry in origin:
            entry.remove_translation_records()
            entry.update_po_file()
    else:
        origin.remove_translation_records()
        origin.update_po_file()