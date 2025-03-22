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
from os import listdir, linesep, unlink
from web.models import TRANSLATIONS
from web.management.commands.language import Command as LanguageCommand
from django.core.management.base import BaseCommand 
from logging import getLogger, ERROR
from os.path import join
from kuusi.settings import LOCALE_PATHS, AVAILABLE_LANGUAGES, DEFAULT_LANGUAGE_CODE
from termcolor import colored, COLORS
logger = getLogger("command")


class Command(BaseCommand):
    help = "Generate and read text files to update translations"

    def add_arguments(self, parser):
        parser.add_argument("lang_code",  type=str)
        parser.add_argument("path", type=str)
        parser.add_argument("--read", action="store_true", default=False)

    def dump(self, path: str, wanted_lang: str):
        for lang in AVAILABLE_LANGUAGES:
            lang_code = lang[0]
            if lang_code != DEFAULT_LANGUAGE_CODE and lang_code == wanted_lang:
                missing = []
                for key, value in TRANSLATIONS[lang_code].items():

                    default_value = TRANSLATIONS[DEFAULT_LANGUAGE_CODE][key]
                    if  default_value is not None  and value == None:
                        missing.append(default_value + linesep)
                
                lang_path = join(path, f"{lang_code}.txt")
                logger.info(f"Locale {colored(lang_code, 'magenta')} has {colored(len(missing), 'red')} missing values.")
                with open(lang_path, "w") as file:
                    file.writelines(missing)

    def read(self, path: str, wanted_lang: str):
        for lang in AVAILABLE_LANGUAGES:
            lang_code = lang[0]
            if lang_code != DEFAULT_LANGUAGE_CODE and wanted_lang == lang_code:
                full_path = join(path, f"{lang_code}.txt")
                if exists(full_path):
                    lines = open(full_path, "r").readlines()
                    lines = [l.replace("\n","") for l in lines]

                    missing = []
                    for key, value in TRANSLATIONS[lang_code].items():
                        default_value = TRANSLATIONS[DEFAULT_LANGUAGE_CODE][key]
                        if  default_value is not None  and value == None:
                            missing.append(key)
                    if len(missing) != len(lines):
                        logger.error(f"Mismatch of keys and values ({colored(len(missing), 'red')}vs{colored(len(lines), 'green')})")
                    else:
                        for i in range(0, len(missing)):
                            lang_key = missing[i]
                            lang_value = lines[i]
                            LanguageCommand.update_locale_files(lang_code, lang_key, lang_value)
                        unlink(full_path)


    def handle(self, *args, **options):
        path = options["path"]
        read = options["read"]
        lang = options["lang_code"]
        if not read:
            self.dump(path, lang)
        else:
            self.read(path, lang)
