"""
distrochooser
Copyright (C) 2014-2026 Christoph Müller <mail@chmr.eu>

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

from typing import Dict, List, Callable, Any
from web.models import FacetteAssignment, Choosable, Facette
from logging import getLogger
from django.db.models import Q

logger = getLogger("command")


def create_assignments(
    get_or_default: Callable[[str, Dict], Any], haystack: Dict
) -> List[FacetteAssignment]:
    got = []
    FacetteAssignment.objects.update(is_invalidated=True)
    for element, data in haystack.items():        
        old_assignment = FacetteAssignment.objects.filter(catalogue_id=element)

        # Create a source string
        sources_str = None
        if "sources" in data:
            sources_str = ",".join(data["sources"])
            sources_str = sources_str.strip(",")
        new_assignment = FacetteAssignment(
            catalogue_id=element,
            description=f"{element}-description",
            assignment_type=data["how"].upper(),
            is_invalidated=False,
            sources = sources_str 
        )
        if old_assignment.count() != 0:
            logger.info(
                f"There is an old assignment with catalogue_id={element}. Attempting re-use"
            )
            new_assignment.pk = old_assignment.first().pk

        new_assignment.save()

        new_assignment.choosables.set(
            Choosable.objects.filter(Q(name__in=data["choosables"]) | Q(catalogue_id__in=data["choosables"]))
        )
        new_assignment.facettes.set(
            Facette.objects.filter(catalogue_id__in=data["facettes"])
        )

        new_assignment.save()
        got.append(new_assignment)

    # delete old, unused ones
    objects = FacetteAssignment.objects.filter(is_invalidated=True)
    logger.info(f"Removing {objects.count()} orphan facette assignments.")
    objects.delete()
    return got
