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

from web.models import LanguageFeedback
from django.core.management.base import BaseCommand
from logging import getLogger, ERROR

logger = getLogger('command')

class Command(BaseCommand):
    help = "Review provided language feedback"
    def add_arguments(self, parser):
        parser.add_argument("lang_code", type=str)
    def handle(self, *args, **options):
        lang_code = options["lang_code"]
        data = LanguageFeedback.objects.filter(session__language_code=lang_code)
        for element in data:
            print(f"{element.pk} {element.language_key} => {element.value}")
            # ADD crud interface for review
            # Store accepted translations in files
            # Remove suggestions
