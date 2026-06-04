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

from django.apps import AppConfig
from os.path import exists, join
from kuusi.settings import GIT_HASH_PATH
from os import environ

class WebConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "web"
    def ready(self):
        from web.util import hot_load_translations
        hot_load_translations()

        # See ADR 0028
        # Attempt to identify git hash to identify changed environments

        if exists(GIT_HASH_PATH):
            environ["GIT_HASH"] = open(GIT_HASH_PATH, "r").read()
