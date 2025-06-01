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

from re import finditer, Match
from pathlib import Path, PurePath
from posixpath import abspath, dirname, isabs, join
from django.core.management.base import BaseCommand
from tomllib import loads
from typing import Dict, List
from django.core.cache import cache


from web.models import TranslateableFieldRecord, Widget, Facette, Category, FacetteAssignment, Choosable, FacetteBehaviour, Page, SessionVersion
from web.management.commands.modules.parse import create_version, create_pages, create_categories, create_widgets, create_choosables, create_facettes, create_facette_behaviours, create_assignments

from logging import getLogger, ERROR

logger = getLogger('command')

class Command(BaseCommand):
    help = "Imports a given *.ku file"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def resolve(self, file_path: str) -> str:
        """
        Return the TOML contents as a string, includes resolved.
        """
        content = open(file_path, "r").read()
        path_file = Path(file_path)
        folder_path = path_file.parent.resolve()


        matches = finditer(r"#include\s{1,}([^\n]+)", content)

        match: Match
        for match in matches:
            full_match = match.group(0)
            raw_path = match.group(1)
            full_file_path = PurePath(folder_path, raw_path)

            included_content = self.resolve(full_file_path)
            content = content.replace(full_match, included_content)
    
        return content

    def handle(self, *args, **options):
        
        file_path = options["file_path"]
        
        got = self.resolve(file_path)
        parsed_toml = loads(got)


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
        
        # This components have no binding towards the result -> just delete them and start over
        Page.objects.all().delete()
        Category.objects.all().delete()
        Widget.objects.all().delete()
        new_pages = create_pages(self.get_or_default, parsed_toml["page"])
        new_categories = create_categories(self.get_or_default, parsed_toml["category"])
        new_widgets = create_widgets(self.get_or_default, parsed_toml["widget"])

        # Versions are bound to results and sessions -> do "light" recreation only
        new_versions = create_version(self.get_or_default, parsed_toml["version"])

        # Choosables will be re-used, if possible
        new_choosables = create_choosables(self.get_or_default, parsed_toml["choosable"])

        # facettes will be re-used, if possible
        new_facettes = create_facettes(self.get_or_default, parsed_toml["facette"])

        # Assignments will attempt re-use
        new_assignments = create_assignments(self.get_or_default, parsed_toml["assignment"])

        # Behaviours will be wiped upon running this method
        new_behaviours = create_facette_behaviours(self.get_or_default, parsed_toml["behaviour"])

        cache.clear()
        logger.info("")
        logger.info(f"Summary for file {file_path}")
        logger.info("")
        logger.info(f"Created/ updated {len(new_versions)} versions. In DB={SessionVersion.objects.all().count()}")
        logger.info(f"Created/ updated {len(new_pages)} pages. In DB={Page.objects.all().count()}")
        logger.info(f"Created/ updated {len(new_categories)} categories. In DB={Category.objects.all().count()}")
        logger.info(f"Created/ updated {len(new_widgets)} widgets. In DB={Widget.objects.all().count()}")
        logger.info(f"Created/ updated {len(new_choosables)} choosables. In DB={Choosable.objects.all().count()}")
        logger.info(f"Created/ updated {len(new_facettes)} facettes. In DB={Facette.objects.all().count()}")
        logger.info(f"Created/ updated {len(new_assignments)} assignments. In DB={FacetteAssignment.objects.all().count()}")
        logger.info(f"Created/ updated {len(new_behaviours)} behaviours. In DB={FacetteBehaviour.objects.all().count()}")
        
        
        
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
            "css_classes": None,
            "bg_color": "black",
            "fg_color": "white"
        }
        if prop in raw:
            return raw[prop]
        if prop in defaults:
            return defaults[prop]
        
        return None
    


   
