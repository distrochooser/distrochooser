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
from typing import Dict, List, Callable
from web.models import Facette, FacetteBehaviour
from logging import getLogger


logger = getLogger('command') 
def create_facettes(get_or_default: Callable[[str, Dict], any], haystack: Dict) -> List[Facette]:
    got = []
    Facette.objects.all().update(
        is_invalidated = True
    )
    for element, data in haystack.items():
        existing_facette = Facette.objects.filter(catalogue_id=element)
        new_facette = Facette(
            catalogue_id = element,
            topic = data["topic"],
            is_invalidated=False
        )

        if existing_facette.count() != 0:
            new_facette.pk = existing_facette.first().pk
            logger.info(f"There is a facette with catalogue_id={element}. Re-Using PK.")

        new_facette.save()
        got.append(new_facette)
    
    # delete old, unused ones
    objects = Facette.objects.filter(is_invalidated=True)
    logger.info(f"Removing {objects.count()} orphan facettess.")
    objects.delete()
    return got

def create_facette_behaviours(get_or_default: Callable[[str, Dict], any], haystack: Dict) -> List[FacetteBehaviour]:
    got = []

    # We won't preserve behaviours.
    FacetteBehaviour.objects.all().delete()

    for element, data in haystack.items():
        new_behaviour = FacetteBehaviour(
            catalogue_id = element,
            description = element,
            direction = data["direction"].upper(),
            criticality = data["criticality"].upper()
        )

        new_behaviour.save()

        new_behaviour.affected_objects.set(Facette.objects.filter(catalogue_id__in=data["objects"]))
        new_behaviour.affected_subjects.set(Facette.objects.filter(catalogue_id__in=data["subjects"]))
        new_behaviour.save()
        got.append(new_behaviour)
    return got