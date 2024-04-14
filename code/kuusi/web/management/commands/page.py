from typing import Dict, List, Callable
from web.models import Page, SessionVersion
from logging import getLogger

logger = getLogger('command') 
def create_pages(get_or_default: Callable[[str, Dict], any], haystack: Dict) -> List[Page]:
        """
        Create the pages in two loops:
        1. Create the pages without next_page set
        2. Update the page with the next_page (if any)
        """
        got = []
        
        # Create the stub pages in the first loop
        for catalogue_id, properties in haystack.items():
            logger.info(f"Current: {catalogue_id}")
            new_page = Page(
                catalogue_id = catalogue_id,
                can_be_marked = get_or_default("can_be_marked", properties),
                require_session  = get_or_default("require_session", properties)
            )
            new_page.save()
            
        # Assign the next pages after all pages are created
        for catalogue_id, properties in haystack.items():
            page = Page.objects.get(catalogue_id=catalogue_id)
            next_catalogue_id = properties["next_page"]
            logger.info(f"Trying to assign next page from {next_catalogue_id} to {page}")
            page.next_page =  Page.objects.get(catalogue_id=next_catalogue_id)
            not_in_versions = get_or_default("not_in_versions", properties)

            if len(not_in_versions) > 0:
                version_name: str
                for version_name in not_in_versions:
                    page.not_in_versions.add(SessionVersion.objects.get(version_name=version_name))

            page.save()
            got.append(page)

        return got

        