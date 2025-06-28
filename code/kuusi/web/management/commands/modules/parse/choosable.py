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
from typing import Dict, List, Callable, Any
from web.models import Choosable, ChoosableMeta
from logging import getLogger


logger = getLogger('command') 
def create_choosables(get_or_default: Callable[[str, Dict], Any], haystack: Dict) -> List[Choosable]:
    got = []
    # Meta will just be re-created
    ChoosableMeta.objects.all().delete()
    Choosable.objects.all().update(
        is_invalidated=True
    )
    for element in haystack:
        catalogue_id = element["catalogue_id"]

        new_choosable = Choosable(
            catalogue_id = catalogue_id,
            name = catalogue_id,
            fg_color = get_or_default("fg_color", element),
            bg_color = get_or_default("bg_color", element),
            is_invalidated=False
        )

        existing_choosables = Choosable.objects.filter(
            catalogue_id = catalogue_id
        )
        if existing_choosables.count() != 0:
            new_choosable.pk = existing_choosables.first().pk
            logger.info(f"There is already a choosable with catalogue_id={catalogue_id}. Re-Using PK.")

        new_choosable.save()
        
        # Only assign meta values if there are any
        if "meta" in element:
            for meta in element["meta"]:
                new_choosable_meta = ChoosableMeta(
                    catalogue_id = meta["meta_name"],
                    meta_choosable = new_choosable,
                    meta_name = meta["meta_name"].upper(),
                    meta_value = meta["meta_value"]
                )
                new_choosable_meta.save()

        got.append(new_choosable)
    
    # delete old, unused ones
    objects = Choosable.objects.filter(is_invalidated=True)
    logger.info(f"Removing {objects.count()} orphan choosables")
    objects.delete()
    return got