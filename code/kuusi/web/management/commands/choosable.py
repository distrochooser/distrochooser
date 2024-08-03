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
from web.models import Choosable, ChoosableMeta
from logging import getLogger


logger = getLogger('command') 
def create_choosables(get_or_default: Callable[[str, Dict], any], haystack: Dict) -> List[Choosable]:
    got = []

    for element in haystack:
        catalogue_id = element["catalogue_id"]

        new_choosable = Choosable(
            catalogue_id = catalogue_id,
            name = catalogue_id,
            fg_color = get_or_default("fg_color", element),
            bg_color = get_or_default("bg_color", element)
        )
        new_choosable.save()
        # Only assign meta values if there are any
        if "meta" in element:
            for meta in element["meta"]:
                new_choosable_meta = ChoosableMeta(
                    catalogue_id = meta["meta_name"],
                    meta_choosable = new_choosable,
                    meta_type = meta["meta_type"],
                    meta_name = meta["meta_name"],
                    meta_value = meta["meta_value"]
                )
                new_choosable_meta.save()

        got.append(new_choosable)
    return got