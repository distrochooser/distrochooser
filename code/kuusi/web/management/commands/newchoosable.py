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

from django.core.management.base import BaseCommand
from logging import getLogger
from web.models import Choosable, ChoosableMeta
logger = getLogger("command")


class Command(BaseCommand):
    help = "Add a new skeleton for a choosable"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)
        parser.add_argument("--catalogue_id", required=True, type=str, help="catalogue ID of the new choosable")
    
    def handle(self, *args, **options):
        file_path = options["file_path"]

        new_content = "\n"
        c = Choosable()
        c.catalogue_id = "test"
        c.name = "test"
        c.bg_color = "test"
        c.fg_color = "test"

        data = c.as_toml()
        new_content += data

        for value in ChoosableMeta.MetaName.values:
            m = ChoosableMeta()
            m.meta_name = value
            m.meta_value = ""
            m.meta_choosable = c

            meta_data = m.as_toml()
            new_content += meta_data
        
        

        with open(file_path, "a") as file:
            file.write(new_content)
