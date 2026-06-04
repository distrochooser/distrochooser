"""
distrochooser
Copyright (C) 2014-2026 Christoph Müller <distrochooser@chmr.eu>

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

from pathlib import Path, PurePath
from re import finditer, Match

def get_matrix_content(file_path: str) -> str:
    """
    Return the TOML contents as a string, includes resolved.
    """
    content = open(file_path, "r").read()
    path_file = Path(file_path)
    folder_path = path_file.parent.resolve()


    matches = finditer(r"#include\s{1,}([^\n]+)", content)

    match: Match
    for match in matches:
        full_match = match.group(0)
        raw_path = match.group(1)
        full_file_path = PurePath(folder_path, raw_path)

        included_content = get_matrix_content(str(full_file_path))
        content = content.replace(full_match, included_content)

    return content