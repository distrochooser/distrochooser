"""
distrochooser
Copyright (C) 2014-2026 Christoph Müller <distrochooser@chmr.eu>

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

from django.core.management.base import BaseCommand, CommandParser
from web.models.session import Session
from termcolor import colored
from kuusi.settings import DEBUG


class Command(BaseCommand):
    help = "Dev tools, only available in DEBUG"

    def add_arguments(self, parser: CommandParser):
        parser.add_argument("--reset", action="store_true", default="false")
        parser.add_argument("--resetunimported", action="store_true", default="false")

    def handle(self, *args, **options):
        if not DEBUG:
            raise Exception("Only available in DEBUG mode")
        if options["reset"]:
            self.reset(False)
        if options["resetunimported"]:
            self.reset(True)

    def reset(self, unimported: bool):
        got, _ = Session.objects.filter(
            imported_from_session__isnull=unimported
        ).delete()
        print(f"Deleted {colored(got, 'magenta')} sessions")
