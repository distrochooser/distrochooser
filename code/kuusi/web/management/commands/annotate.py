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
from os import unlink, walk
from web.models import TRANSLATIONS, Page
from web.management.commands.languagefeedback import Command as LanguageCommand
from django.core.management.base import BaseCommand
from logging import getLogger
from os.path import join, isdir
from pathlib import Path
from kuusi.settings import AVAILABLE_LANGUAGES, DEFAULT_LANGUAGE_CODE
from termcolor import colored
from re import match, Pattern, compile

logger = getLogger("command")


class Command(BaseCommand):
    help = "Annotate assingment toml data with translations"

    kuusi_prefix = "# distrochooser::"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)
        parser.add_argument("--remove", action="store_true", default=False, help="Remove the annotations, if any")
        parser.add_argument("--markdown", action="store_true", default=False, help="Return the summary as markdown")
        parser.add_argument("--lang", nargs="*",help="limit languages to be checked for", default=[],)

    def annotate_block(self, pattern: str, line: str, search_for: str, explicit_lang_list: List[str]) -> Tuple[str| None, List[str], List[str]]:
        new_lines = []

        missing_languages = []
        catalogue_id= None
        if not line.startswith(self.kuusi_prefix):
            result = match(pattern, line)
            if result is not None:
                annotation = (
                    f"{self.kuusi_prefix}translation::{DEFAULT_LANGUAGE_CODE}::"
                )
                groups = result.groupdict()
                catalogue_id = groups['catalogue_id']
                translation = f"{catalogue_id}-{search_for}"

                # Special handling for pages, some elements might not be needed at all
                stop = False
                if "page" in pattern:
                    page_obj = Page.objects.get(catalogue_id=catalogue_id)
                    if page_obj.hide_help and  search_for == "text":
                        stop = True


                
                if not stop:
                    if translation in TRANSLATIONS[DEFAULT_LANGUAGE_CODE]:
                        default_translation = TRANSLATIONS[DEFAULT_LANGUAGE_CODE][
                            translation
                        ]
                        annotation = annotation + default_translation + "\n"
                    else:
                        annotation = annotation + "None\n"  #

                    annotation = (
                        annotation + f"{self.kuusi_prefix}translation::key::{translation}\n"
                    )
                    for lang_tuple in AVAILABLE_LANGUAGES:
                        
                        lang = lang_tuple[0]
                        continue_check = explicit_lang_list.__len__() > 0 and lang in explicit_lang_list or explicit_lang_list.__len__() == 0
                        if continue_check:
                            is_lang_there = lang in TRANSLATIONS
                            if is_lang_there:
                                is_translation_missing = translation not in TRANSLATIONS[lang]
                                if is_translation_missing:
                                    missing_languages.append(lang)
                                else: 
                                    if lang != DEFAULT_LANGUAGE_CODE:
                                        english_value = TRANSLATIONS[DEFAULT_LANGUAGE_CODE][translation]
                                        translation_value = TRANSLATIONS[lang][translation]
                                        still_english_value =english_value == translation_value
                                        if still_english_value:
                                            missing_languages.append(lang)

                    missing_languages_str = (",".join(missing_languages)).strip(",")
                    if missing_languages.__len__() > 0:
                        annotation += f"{self.kuusi_prefix}issue::missing translation::{missing_languages_str}\n"
                    new_lines.append(annotation)

        missing_languages.sort()
        return catalogue_id, new_lines, missing_languages

    def handle_file(self, file_path: str, remove: bool, explicit_lang_list: List[str], markdown: bool):

        new_lines = []
        summary_text = {}
        """
        Iterate all lines of the file

        search for assignment. and add infos above, such as:
        - Default value (taken from DEFAULT_LANGUAGE_CODE)
        - Missing translations (listing just the code)
        """
        path_info = Path(file_path)
        with open(file_path, "r") as file:
            raw_contents = file.readlines()
            contents = list(filter(lambda l: not l.startswith(self.kuusi_prefix), raw_contents))
            for index, line in enumerate(contents):
                if not remove:
                    additions = []
                    blocks = {
                        r"\[\s{0,}assignment.(?P<catalogue_id>[^[\]]+)": [
                            "description"
                        ],
                        r"\[\s{0,}facette.(?P<catalogue_id>[^[\]]+)": [
                            "description"
                        ],
                        r"\[\s{0,}choosable.(?P<catalogue_id>[^[\]\.]+)": [
                            "description"
                        ],
                        r"\[\s{0,}version.(?P<catalogue_id>[^[\]\.]+)": [
                            "description",
                        ],
                        r"\[\s{0,}page.(?P<catalogue_id>[^[\]\.]+)": [
                            "text",
                            "title"
                        ],
                    }

                    for block, search_for in blocks.items():
                        exit_block = False
                        for element in search_for:
                            catalogue_id, additions, missing_languages = self.annotate_block(block, line, element, explicit_lang_list)
                            if additions.__len__() != 0:
                                new_lines += additions
                                if missing_languages.__len__() != 0: 
                                    summary_text[line] = f"File={colored(path_info.name, color='cyan')} Component={colored(line.strip(), color='blue')} Key={colored(f'{catalogue_id}-{element}', color='light_magenta')} Missing={colored(','.join(missing_languages), color='yellow')}"
                                
                                exit_block = True
                        
                        if exit_block:
                            break
                    new_lines.append(line)
                else:
                    # remove annotations
                    if not line.startswith(self.kuusi_prefix):
                        new_lines.append(line)

        with open(file_path, "w") as file:
            for line in new_lines:
                file.write(line)

        new_content = open(file_path, "r").readlines()
        collected_markdown =""
        if not remove: 
            for matched_line, text in summary_text.items():
                if markdown:
                    # TODO: This is awfully disgusting
                    ansi_escape = compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
                    parts = ansi_escape.sub('', text).split("=")
                    
                    file = parts[1].replace(" Component", "")
                    element = parts[2].replace(" Key", "")
                    key = parts[3].replace(" Missing", "")
                    missing_langs = parts[4]
                    collected_markdown += f"🧩 {element}: 🔑 {key} -> 🗣️: {missing_langs}\n\n"
                else:
                    line_number = new_content.index(matched_line) + 1
                    print(f"Line={colored(line_number, color='red')} {text}")
                
        
        if markdown and len(collected_markdown) > 0:
            print(f"<details><summary>{file_path}</summary>");
            print(collected_markdown)
            print(f"</details>");
    
    def handle(self, *args, **options):
        file_path = options["file_path"]
        remove = options["remove"]
        lang = options["lang"]
        markdown = options["markdown"]

        if isdir(file_path):
            result = [
                join(dp, f)
                for dp, dn, filenames in walk(file_path)
                for f in filenames
                if f.endswith(".toml")
            ]
            for file in result:
                self.handle_file(file, remove, lang, markdown)
        else:
            self.handle_file(file_path, remove, lang, markdown)
