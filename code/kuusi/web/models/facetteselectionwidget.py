"""
kuusi
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

from typing import Tuple, Dict, List
from django.db import models
from web.models import Facette
from web.models import Session, Widget, FacetteSelection, Page, WebHttpRequest
from web.forms import WarningForm
from django.template import loader
from django.forms import Form, BooleanField
from web.helper import trigger_behaviours, get_active_facettes

from logging import getLogger

logger = getLogger("root")

class FacetteSelectionWidget(Widget):
    topic = models.CharField(null=False, blank=False, max_length=120)