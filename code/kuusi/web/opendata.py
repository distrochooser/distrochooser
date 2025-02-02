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

from typing import Dict

class OpenDataV1():
    def __init__(self):
        self.ChoosableClicks : Dict[str, int] = {} # The clicks per choosable to the choosable's website
        self.FinishedTests: int = 0 # Tests finished (acknowledged)
        self.Tests: int = 0 # All Tests Count
        self.TestsFromOthers: int = 0 # Tests derived from other tests (origin not null)
        self.TestsAllVersions = 0 # All Tests over all versions 
        self.AccessibilityOptionsActive: Dict[str, int] = {} # Map of option name and active sets
        self.FeedbackGiven: int = 0 #How many assignments have been reported
        self.FeedbackGivenFlaggedAssignments: Dict[str, int] = {} # What assignments have been reported
        self.OS_Families:  Dict[str, int] = {}
        self.Browser_Families:  Dict[str, int] = {}
        self.Bots:  Dict[str, int] = {}

        self.RefreshInterval = 60*60*24
        self.IsCached = False
        self.NextUpdate = 0
        self.OpenDataLicense = "ODbL-1.0"