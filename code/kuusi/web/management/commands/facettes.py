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
from typing import Dict, List, Callable
from web.models import Facette, FacetteBehaviour
from logging import getLogger


logger = getLogger('command') 
def create_facettes(get_or_default: Callable[[str, Dict], any], haystack: Dict) -> List[Facette]:
    got = []

    for element, data in haystack.items():
        new_facette = Facette(
            catalogue_id = element,
            topic = data["topic"]
        )

        new_facette.save()
        got.append(new_facette)
    return got

def create_facette_behaviours(get_or_default: Callable[[str, Dict], any], haystack: Dict) -> List[FacetteBehaviour]:
    got = []

    for element, data in haystack.items():
        new_behaviour = FacetteBehaviour(
            catalogue_id = element, # TODO: Redundancy between .name and .catalogue_id
            description = f"{element}",
            direction = data["direction"].upper(),
            criticality = data["criticality"].upper()
        )

        new_behaviour.save()

        new_behaviour.affected_objects.set(Facette.objects.filter(catalogue_id__in=data["objects"]))
        new_behaviour.affected_subjects.set(Facette.objects.filter(catalogue_id__in=data["subjects"]))
        new_behaviour.save()
        got.append(new_behaviour)
    return got