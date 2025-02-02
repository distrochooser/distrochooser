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
from web.models import Category, Page
from logging import getLogger


logger = getLogger('command') 
def create_categories(get_or_default: Callable[[str, Dict], any], haystack: Dict) -> List[Category]:
    """
    Create cateogries in two steps:
    1. Create stub categories
    2. Assign child and parent relation
    """
    got = []
    for catalogue_id, properties in haystack.items():
        logger.info(f"Current: {catalogue_id}")
        
        new_category = Category(
            catalogue_id=catalogue_id, # preserve the catalogue id for translation purposes to uniquely identify the translateable field
            name=catalogue_id,
            icon=get_or_default("icon", properties),
            identifier = catalogue_id,
            target_page = Page.objects.get(catalogue_id=properties["target_page"])
        )
        new_category.save()
    
    for catalogue_id, properties  in haystack.items():
        child_of = get_or_default("child_of", properties)
        category_child = Category.objects.get(identifier=catalogue_id) # Always query the "child" to collect it for return
        if child_of:
            category_child.child_of = Category.objects.get(catalogue_id=child_of)
            category_child.save()
        got.append(category_child)
    return got