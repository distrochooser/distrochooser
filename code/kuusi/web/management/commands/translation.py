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
from typing import List, Tuple
from genericpath import exists
from os import unlink
from web.models import TRANSLATIONS, Choosable
from web.management.commands.language import Command as LanguageCommand
from django.core.management.base import BaseCommand 
from logging import getLogger
from os.path import join
from kuusi.settings import  AVAILABLE_LANGUAGES, DEFAULT_LANGUAGE_CODE
from termcolor import colored
logger = getLogger("command")


class Command(BaseCommand):
    help = "Generate and read text files to update translations"
    line_sep = "|||\n" # if users desire to use services for translation, use asome kind of 'identifiable' line sep rather than \n

    def add_arguments(self, parser):
        parser.add_argument("lang_code",  type=str)
        parser.add_argument("path", type=str)
        parser.add_argument("--read", action="store_true", default=False)
        parser.add_argument("--dry_run", action="store_true", default=False)
        parser.add_argument("--mask", action="store_true", default=False)

    def dump(self, path: str, wanted_lang: str, mask: bool):
        for lang in AVAILABLE_LANGUAGES:
            lang_code = lang[0]
            if lang_code != DEFAULT_LANGUAGE_CODE and lang_code == wanted_lang:
                _, missing= self.get_missing_values(lang_code, mask)
                
                lang_path = join(path, f"{lang_code}.txt")
                logger.info(f"Locale {colored(lang_code, 'magenta')} has {colored(len(missing), 'red')} missing values.")
                if len(missing) != 0:
                    with open(lang_path, "w") as file:
                        file.writelines(missing)
                else:
                    logger.info("Not creating a file")

    def mask(self, value: str, do_masking: bool) -> str:
        # Sometimes, translators attempt to translate this aswell -> omit it
        if not do_masking:
            return value
        return value.replace("distrochooser", "###").replace("Distrochooser", "###")
    
    def unmask(self, value: str) -> str:
        return value.replace("###", "distrochooser")

    def get_missing_values(self, lang_code, mask: bool) -> Tuple[List[str], List[str]]:
        missing = []
        missing_key = []
        # Excempt the choosables names, because they shall not be translated at all
        choosables = Choosable.objects.all()
        exceptions = []
        for choosable in choosables:
            exceptions.append(f"{choosable.catalogue_id}-name")
        for key, default_value in TRANSLATIONS[DEFAULT_LANGUAGE_CODE].items():
            if key not in exceptions: # Avoid translating names
                lang_value =TRANSLATIONS[lang_code][key] if  lang_code in TRANSLATIONS and key in TRANSLATIONS[lang_code] else None
                if lang_value is not None:
                    lang_value = self.mask(lang_value.strip(), mask)
                value = f"{lang_value}{self.line_sep}"

                if  default_value is not None  and lang_value == default_value and len(value) != "":
                    missing.append(self.mask(value, mask))
                    missing_key.append(key)

                if default_value is not None and lang_value is None:
                    default_replacement = self.mask(TRANSLATIONS[DEFAULT_LANGUAGE_CODE][key].strip(), mask)
                    value = f"{default_replacement}{self.line_sep}"
                    missing.append(value)
                    missing_key.append(key)
            
        return missing_key, missing


    def read(self, path: str, wanted_lang: str, dry_run: bool=False):
        for lang in AVAILABLE_LANGUAGES:
            lang_code = lang[0]
            if lang_code != DEFAULT_LANGUAGE_CODE and wanted_lang == lang_code:
                full_path = join(path, f"{lang_code}.txt")
                if exists(full_path):
                    lines = open(full_path, "r").readlines()
                    lines = [l.replace(self.line_sep,"") for l in lines]

                    missing_key, missing = self.get_missing_values(lang_code, False)
                    if len(missing_key) != len(lines):
                        logger.error(f"Mismatch of keys and values ({colored(len(missing), 'red')}vs{colored(len(lines), 'green')})")
                    else:
                        for i in range(0, len(missing_key)):
                            lang_key = missing_key[i]
                            lang_value = self.unmask(lines[i])
                            if not dry_run:
                                LanguageCommand.update_locale_files(lang_code, lang_key, lang_value) # type: ignore
                            else:
                                logger.debug(f"Would update as following: {lang_key} -> {lang_value}")
                        if not dry_run:
                            unlink(full_path)


    def handle(self, *args, **options):
        path = options["path"]
        read = options["read"]
        mask = options["mask"]
        lang = options["lang_code"]
        dry_run = options["dry_run"]
        if not read:
            self.dump(path, lang, mask)
        else:
            self.read(path, lang, dry_run)
