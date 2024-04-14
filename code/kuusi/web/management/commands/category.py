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