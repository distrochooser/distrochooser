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

from genericpath import exists
from json import dumps, loads
from os import listdir
from web.models import LanguageFeedback
from django.core.management.base import BaseCommand
from logging import getLogger, ERROR
from os.path import join
from kuusi.settings import LOCALE_PATHS

logger = getLogger("command")


class Command(BaseCommand):
    help = "Review provided language feedback"

    def add_arguments(self, parser):
        parser.add_argument("lang_code", type=str)
        parser.add_argument("--delete", type=int, nargs="*")
        parser.add_argument("--approve", type=int, nargs="*")
        parser.add_argument("--clear", action="store_true", default=False)
        parser.add_argument("--persist", action="store_true", default=False)

    def update_locale_files(lang_code: str, lang_key: str, lang_value:str ): # type: ignore
        lang_code = lang_code.strip()
        lang_key = lang_key.strip()
        lang_value = lang_value.strip()
        target_path = LOCALE_PATHS[0]
        files = listdir(target_path)

        was_found = False
        for file in files:
            needs_update = False
            if file.endswith("json") and file.endswith(
                f"-{lang_code}.json"
            ):
                old_data = {}
                json_path = join(target_path, file)
                if exists(json_path):
                    old_data = loads(open(json_path, "r").read())
                if lang_key in old_data:
                    needs_update = True
                    was_found = True
                    old_data[lang_key] = lang_value

                if needs_update:
                    print(f"File {json_path} will be updated")
                    with open(json_path, "w") as file:
                        file.write(dumps(old_data, ensure_ascii=False))

        if not was_found:
            # Create and update the additional-<lang code>.json if needed
            print(f"The value {lang_key} was not found. Putting it into additional json file")
            old_data = {}
            json_path = join(target_path, f"additional-{lang_code}.json")
            if exists(json_path):
                old_data = loads(open(json_path, "r").read())
            old_data[lang_key] = lang_value

            print(f"File {json_path} will be updated")
            with open(json_path, "w") as file:
                file.write(dumps(old_data, ensure_ascii=False))
            


    def handle(self, *args, **options):
        lang_code = options["lang_code"]
        to_delete = options["delete"]
        to_approve = options["approve"]
        remove_unapproved = options["clear"]
        to_persist = options["persist"]
        if to_delete is not None:
            for pk in to_delete:
                LanguageFeedback.objects.filter(pk=pk).delete()
        if to_approve is not None:
            for pk in to_approve:
                obj = LanguageFeedback.objects.filter(pk=pk).first()
                obj.is_approved = not obj.is_approved
                obj.save()
                LanguageFeedback.objects.filter(
                    session__language_code=lang_code
                ).filter(language_key=obj.language_key).exclude(pk=pk).delete()
        if remove_unapproved:
            LanguageFeedback.objects.filter(session__language_code=lang_code).exclude(
                is_approved=True
            ).delete()
        data = LanguageFeedback.objects.filter(session__language_code=lang_code)
        for element in data:
            print(
                f"[{'X' if element.is_approved else ' '}] {element.pk} {element.language_key} => {element.value}"
            )

        if to_persist is not None:
            for element in data:
                if element.is_approved:
                    Command.update_locale_files(lang_code, element.language_key, element.value)
                    element.delete()


