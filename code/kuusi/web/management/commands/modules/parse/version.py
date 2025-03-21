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
from web.models import SessionVersion
from logging import getLogger

logger = getLogger('command')

def create_version(_: Callable, haystack: Dict) -> List[SessionVersion]:
    """
    Create versions from the haystack
    """
    results = []
    for catalogue_id, _ in haystack.items():
        logger.info(f"New version: {catalogue_id}")
        with_same_catalogue_id = SessionVersion.objects.filter(
            catalogue_id=catalogue_id,
            version_name=catalogue_id
        )
        if with_same_catalogue_id.count() == 0:
            new_version = SessionVersion(
                catalogue_id = catalogue_id,
                version_name = catalogue_id
            )
            new_version.save()
            results.append(new_version)
        else:
            results.append(with_same_catalogue_id)
    
    return results
    