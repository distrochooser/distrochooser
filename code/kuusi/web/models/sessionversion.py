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

from web.models import Widget
from django.db import models
class SessionVersion(models.Model):
    catalogue_id = models.CharField(null=True, blank=True, default=None, max_length=255) 
    description = models.CharField(null=False, blank=False, max_length=120)

    def __str__(self):
        return f"{self.catalogue_id}"

class SessionVersionWidget(Widget):
    pass
 