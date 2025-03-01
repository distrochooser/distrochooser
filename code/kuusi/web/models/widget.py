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

from __future__ import annotations
from django.db import models




class Widget(models.Model):
    row = models.IntegerField(default=1, null=False, blank=False)
    col = models.IntegerField(default=1, null=False, blank=False)
    width = models.IntegerField(default=1, null=False, blank=False)
    pages = models.ManyToManyField(to="Page", blank=True, default=None)
    
    @property
    def widget_type(self) -> str:
        return self.__class__.__name__