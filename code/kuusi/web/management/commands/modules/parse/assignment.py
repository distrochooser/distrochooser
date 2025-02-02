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
from typing import Dict, List, Callable
from web.models import FacetteAssignment, Choosable, Facette
from logging import getLogger


logger = getLogger('command') 
def create_assignments(get_or_default: Callable[[str, Dict], any], haystack: Dict) -> List[FacetteAssignment]:
    got = []

    for element, data in haystack.items():
        new_assignment = FacetteAssignment(
            catalogue_id = element,
            assignment_type = data["how"].upper(),

        )

        new_assignment.save()

        new_assignment.choosables.set(Choosable.objects.filter(name__in=data["to"]))
        new_assignment.facettes.set(Facette.objects.filter(catalogue_id__in=data["from"]))

        new_assignment.save()
        got.append(new_assignment)
    return got