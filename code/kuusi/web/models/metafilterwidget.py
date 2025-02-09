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

from json import dumps, loads
from web.models import Widget, Choosable, FacetteAssignment, Session
from django.db import models
from typing import List

class MetaFilterWidgetElement:
    def __init__(self):
        self.cell_type = None
        self.cell_name = None
        self.cell_func = None
    
    def __str__(self):
        return f"{self.cell_name} ({self.cell_type}) -> {self.cell_func}"
    
    def get_func_map(self):
        func_map = {
            "filter_number_gt": self.filter_number_gt
        }
        return func_map
    
    def verify(self):
        if self.cell_func not in self.get_func_map():
            raise Exception(f"Function {self.cell_func} not found")

    def apply_cell_func(self, obj: Choosable, value: any) -> FacetteAssignment:
        method = self.get_func_map()[self.cell_func]
        return method(obj, value)
    
    def filter_number_gt(self, obj: Choosable, value: any) -> FacetteAssignment:
        if "AGE" not in obj.meta:
            return None
        matches = int(obj.meta["AGE"].years_since) < int(value)
        result = FacetteAssignment(
            catalogue_id = self.cell_name,
            long_description="suitable" if matches else "not-suitable",
            assignment_type=FacetteAssignment.AssignmentType.POSITIVE if matches else FacetteAssignment.AssignmentType.NEGATIVE
        )
        return result


class MetaFilterWidgetStructure:
    """
    Virtual class. do not persist.
    """
    def __init__(self, raw_input: List):
        self.raw_input = raw_input
        self.structure = []
    
    def parse(self):
        for _, row in enumerate(self.raw_input):
            row_list = []
            for _, cell in enumerate(row):
                cell_content = self.get_cell_content(cell)
                row_list.append(cell_content)
            self.structure.append(row_list)
        
    
    def stringify(self):
        return dumps(self.raw_input)
    
    def get_cell_from_structure(self, key: str) -> MetaFilterWidgetElement:
        for line in self.structure:
            for cell in line:
                if cell.cell_name == key:
                    return cell
        return None


    def get_cell_content(self, raw_input: str) -> MetaFilterWidgetElement:
        parts = raw_input.split(".")
        if parts.__len__() != 3:
            raise Exception(f"Cell content not parseable: {raw_input}")
        cell_type = parts[0]
        cell_name = parts[1]
        cell_func = parts[2]
        cell_obj = MetaFilterWidgetElement()
        cell_obj.cell_name = cell_name
        cell_obj.cell_func = cell_func
        cell_obj.cell_type = cell_type
        cell_obj.verify()
        return cell_obj

class MetaFilterWidget(Widget):
    # To keep this simple, this is for now one field instead of an additional nested structure
    structure = models.TextField(default=None, null=True, blank=True)

    @property
    def parsed_structure(self) -> MetaFilterWidgetStructure:
        obj = MetaFilterWidgetStructure(loads(self.structure))
        obj.parse()
        return obj

class MetaFilterValue(models.Model):

    session = models.ForeignKey(
        to=Session,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="meta_filter_value_session",
    )
    key = models.CharField(null=False, blank=False, max_length=255)
    value = models.CharField(null=False, blank=False, max_length=255)