from typing import Dict, List, Callable
from web.models import SessionVersion
from logging import getLogger, ERROR

logger = getLogger('command')

def create_version(_: Callable, haystack: Dict) -> List[SessionVersion]:
    """
    Create versions from the haystack
    """
    results = []
    for catalogue_id, _ in haystack.items():
        logger.info(f"New version: {catalogue_id}")
        new_version = SessionVersion(
            version_name = catalogue_id
        )
        new_version.save()
        results.append(new_version)
    return results
    