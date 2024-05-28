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

from re import finditer, Match
from pathlib import Path
from posixpath import abspath, dirname, isabs, join
from django.core.management.base import BaseCommand
from tomllib import loads
from typing import Dict, List


from web.models import TranslateableFieldRecord, Widget, Facette, Category, FacetteAssignment, Choosable, FacetteSelection, Page, SessionVersion

from web.management.commands.version import create_version
from web.management.commands.page import create_pages
from web.management.commands.category import create_categories
from web.management.commands.widget import create_widgets
from web.management.commands.choosable import create_choosables
from web.management.commands.facettes import create_facettes, create_facette_behaviours
from web.management.commands.assignment import create_assignments

from logging import getLogger, ERROR

logger = getLogger('command')

class Command(BaseCommand):
    help = "Imports a given *.ku file"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)
        parser.add_argument("--wipe",action='store_true', default=False)

    def wipe_records(self):
        """
        Removes all content from the database
        """
        Choosable.objects.all().delete()
        Facette.objects.all().delete()
        FacetteSelection.objects.all().delete()
        FacetteAssignment.objects.all().delete()
        Category.objects.all().delete()
        Page.objects.all().delete()
        Widget.objects.all().delete()
        SessionVersion.objects.all().delete()
        TranslateableFieldRecord.objects.all().delete()

    def resolve(self, file_path: str) -> str:
        """
        Return the TOML contents as a string, includes resolved.
        """
        content = open(file_path, "r").read()
        file_folder = dirname(abspath(file_path))
        folder_obj = Path(file_folder)

        matches = finditer(r"#include\s{1,}([^\n]+)", content)

        match: Match
        for match in matches:
            full_match = match.group(0)

            full_match_path = folder_obj.joinpath(match.group(1))
            
            included_content = self.resolve(full_match_path)
            content = content.replace(full_match, included_content)
    
        return content

    def handle(self, *args, **options):
        if options["wipe"]:
            self.wipe_records()
        
        file_path = options["file_path"]
        
        got = self.resolve(file_path)
        parsed_toml = loads(got)


        # TODO: Widget: Add defaults if now row/col/width is provided. Defaults:
        """
        row = 1
        col = 1
        width = 12
        """

        # Parse order
        # 1: Versions
        # 2: Pages
        # 3: Categories
        # 4: Widgets
        # 5: Choosables
        # 6: Facettes
        # 7: Assignments
        new_versions = create_version(self.get_or_default, parsed_toml["version"])
        new_pages = create_pages(self.get_or_default, parsed_toml["page"])
        new_categories = create_categories(self.get_or_default, parsed_toml["category"])
        new_widgets = create_widgets(self.get_or_default, parsed_toml["widget"])
        new_choosables = create_choosables(self.get_or_default, parsed_toml["choosable"])
        new_facettes = create_facettes(self.get_or_default, parsed_toml["facette"])
        new_assignments = create_assignments(self.get_or_default, parsed_toml["assignment"])
        new_behaviours = create_facette_behaviours(self.get_or_default, parsed_toml["behaviour"])

        logger.info(f"Summary for file {file_path}")
        logger.info(f"Created {len(new_versions)} versions")
        logger.info(f"Created {len(new_pages)} pages")
        logger.info(f"Created {len(new_categories)} categories")
        logger.info(f"Created {len(new_widgets)} widgets")
        logger.info(f"Created {len(new_choosables)} choosables")
        logger.info(f"Created {len(new_facettes)} facettes")
        logger.info(f"Created {len(new_assignments)} assignments")
        logger.info(f"Created {len(new_behaviours)} behaviours")
        
        
        
    def get_or_default(self, prop: str, raw: str) -> any:
        defaults = {
            "col": 1,
            "row": 1,
            "width": 12,
            "can_be_marked": True,
            "not_in_versions": [],
            "child_of": None,
            "hide_text": False,
            "hide_help": False,
            "css_classes": None
        }
        if prop in raw:
            return raw[prop]
        if prop in defaults:
            return defaults[prop]
        
        return None
    


   
