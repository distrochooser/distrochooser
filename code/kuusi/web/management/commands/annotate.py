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
from typing import List, Tuple, Literal
from genericpath import exists
from os import unlink
from web.models import TRANSLATIONS, Choosable
from web.management.commands.languagefeedback import Command as LanguageCommand
from django.core.management.base import BaseCommand 
from logging import getLogger
from os.path import join
from kuusi.settings import  AVAILABLE_LANGUAGES, DEFAULT_LANGUAGE_CODE
from termcolor import colored
from re import match, Pattern
logger = getLogger("command")


class Command(BaseCommand):
    help = "Annotate assingment toml data with translations"

    kuusi_prefix = "# distrochooser::"
    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)
        parser.add_argument("--remove", action="store_true", default=False)

    def annotate_block(self, pattern: str, line: str) -> List[str]:
        new_lines = []

        if not line.startswith(self.kuusi_prefix):
            result = match(pattern, line)
            if result is not None:
                annotation = f"{self.kuusi_prefix}translation::{DEFAULT_LANGUAGE_CODE}::"
                groups = result.groupdict()
                
                translation = f"{groups['catalogue_id']}-description"
                if translation in TRANSLATIONS[DEFAULT_LANGUAGE_CODE]:
                    default_translation = TRANSLATIONS[DEFAULT_LANGUAGE_CODE][translation]
                    annotation = annotation + default_translation + "\n"
                else:
                    annotation = annotation + "None\n"#

                annotation = annotation + f"{self.kuusi_prefix}translation::key::{translation}\n"
                missing_languages = ""
                for lang_tuple in AVAILABLE_LANGUAGES:
                    lang = lang_tuple[0]
                    is_lang_there = lang in TRANSLATIONS
                    if is_lang_there:
                        is_translation_missing = translation not in TRANSLATIONS[lang] 
                        if is_translation_missing:
                            missing_languages = missing_languages + lang + ","
                        else:
                            if not lang == DEFAULT_LANGUAGE_CODE:
                                is_english = TRANSLATIONS[lang][translation] == TRANSLATIONS[DEFAULT_LANGUAGE_CODE][translation]
                                if is_english:
                                    missing_languages = missing_languages + lang + ","

                missing_languages = missing_languages.strip(",")
                if missing_languages != "":
                    annotation += f"{self.kuusi_prefix}issue::missing translation::{missing_languages}\n"
                new_lines.append(annotation)
                

            new_lines.append(line)

        return new_lines



    def handle(self, *args, **options):
        file_path = options["file_path"]
        new_lines = []

        """
        Iterate all lines of the file

        search for assignment. and add infos above, such as:
        - Default value (taken from DEFAULT_LANGUAGE_CODE)
        - Missing translations (listing just the code)
        """
        with open(file_path, "r") as file:
            contents = file.readlines()
    
            for line in contents:
                if not options["remove"]:
                    additions = []
                    blocks = [
                        r"\[\s{0,}assignment.(?P<catalogue_id>[^[\]]+)",
                        r"\[\s{0,}behaviour.(?P<catalogue_id>[^[\]]+)",
                        r"\[\s{0,}facette.(?P<catalogue_id>[^[\]]+)"
                    ]

                    annotation_done=False
                    for block in blocks:
                        additions = self.annotate_block(block, line)
                        if additions.__len__() != 1:
                            new_lines += additions
                            annotation_done = True
                            break
                    
                    if not annotation_done:
                        new_lines.append(line)
                else:
                    # remove annotations
                    if not line.startswith(self.kuusi_prefix):
                        new_lines.append(line)




        with open(file_path, "w") as file:
            for line in new_lines:
                file.write(line)

                
