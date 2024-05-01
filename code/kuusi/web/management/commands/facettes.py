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
from web.models import Facette
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