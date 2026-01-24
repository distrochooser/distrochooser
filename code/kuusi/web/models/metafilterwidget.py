"""
distrochooser
Copyright (C) 2014-2026 Christoph Müller <mail@chmr.eu>

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
from web.models import Widget, Choosable, FacetteAssignment, Session, Page
from django.db import models
from typing import List, Dict, Any, Tuple
from django.core.cache import cache
from django.db.models.manager import BaseManager

class MetaFilterWidgetElement:
    def __init__(self, type: str, name: str, func: str, args: Any):
        self.cell_type = type
        self.cell_name = name
        self.cell_func = func
        self.cell_arg = args

    def __str__(self):
        return f"{self.cell_name} ({self.cell_type}) -> {self.cell_func}"

    def get_func_map(self):
        func_map = {
            "filter_number_gt": self.filter_number_gt,
            "filter_must_have_assignments": self.filter_must_have_assignments,
            "filter_must_match_language": self.filter_must_match_language,
            "filter_archs": self.filter_archs,
        }
        return func_map

    def verify(self):
        if self.cell_func not in self.get_func_map():
            raise Exception(f"Function {self.cell_func} not found")

    def apply_cell_func(
        self,
        obj: Choosable,
        value: Any,
        collected_assignments: Dict[int, List[FacetteAssignment]],
        session: Session,
    ) -> FacetteAssignment | None:
        if self.cell_func:
            method = self.get_func_map()[self.cell_func]
            return method(obj, value, collected_assignments, session)
        return None

    def filter_must_match_language(
        self, obj: Choosable, value: Any, collected_assignments, session: Session
    ) -> FacetteAssignment | None:
        matches = (
            "LANGUAGES" in obj.meta
            and session.language_code in obj.meta["LANGUAGES"].meta_value
        )
        result = FacetteAssignment(
            catalogue_id=f"{self.cell_name}-"
            + ("suitable" if matches else "not-suitable"),
            description="suitable" if matches else "not-suitable",
            assignment_type=(
                FacetteAssignment.AssignmentType.POSITIVE
                if matches
                else FacetteAssignment.AssignmentType.NEGATIVE
            ),
        )
        result.save()
        return result

    def filter_must_have_assignments(
        self, obj: Choosable, value: Any, collected_assignments, session
    ) -> FacetteAssignment | None:
        if (
            value == "true" and len(collected_assignments) == 0
        ):  # all meta filter values are strings, basically
            result = FacetteAssignment(
                catalogue_id=f"{self.cell_name}-{obj.name}",
                description="not-suitable",
                assignment_type=FacetteAssignment.AssignmentType.BLOCKING,
            )
            result.save()
            return result
        return None

    def filter_number_gt(
        self, obj: Choosable, value: Any, collected_assignments, session
    ) -> FacetteAssignment | None:
        if "AGE" not in obj.meta:
            return None
        matches = int(obj.meta["AGE"].years_since) < int(value)
        result = FacetteAssignment(
            catalogue_id=f"{self.cell_name}-"
            + ("suitable" if matches else "not-suitable"),
            description="suitable" if matches else "not-suitable",
            assignment_type=(
                FacetteAssignment.AssignmentType.POSITIVE
                if matches
                else FacetteAssignment.AssignmentType.NEGATIVE
            ),
        )
        result.save()
        return result

    def filter_archs(
        self, obj: Choosable, value: Any, collected_assignments, session
    ) -> FacetteAssignment | None:
        if "ARCHS" not in obj.meta:
            return None

        # Python dislikes the '' possibly serialized here
        value_parsed = loads(value.replace("'", '"'))
        matched_archs_str = ""
        for arch in value_parsed:
            arch_string = str(arch)
            if arch_string in obj.meta["ARCHS"].as_list:
               matched_archs_str += "," + arch_string
        matched_archs_str = matched_archs_str.strip(",")
        if matched_archs_str != "":
            result = FacetteAssignment(
                catalogue_id=matched_archs_str,
                description=self.cell_name,
                assignment_type=FacetteAssignment.AssignmentType.POSITIVE,
            )
            result.save()
            return result

        # as the choosable has a set of archs, but none matched -> create a negative hit
        # but use the name of the field as translateable catalogue_id
        result = FacetteAssignment(
            catalogue_id="archs",
            description="not-suitable",
            assignment_type=FacetteAssignment.AssignmentType.NEGATIVE,
        )
        result.save()
        return result


class MetaFilterWidgetStructure:
    """
    Virtual class. do not persist.
    """

    def __init__(self, raw_input: List, pk):
        self.raw_input = raw_input
        self.structure = []
        self.original_pk = pk

    def parse(self):
        for _, row in enumerate(self.raw_input):
            row_list = []
            for _, cell in enumerate(row):
                cell_content = self.get_cell_content(cell)
                row_list.append(cell_content)
            self.structure.append(row_list)

    def stringify(self):
        return dumps(self.raw_input)

    def get_cell_from_structure(self, key: str) -> MetaFilterWidgetElement | None:
        cache_key = f"meta-widget-structure-{self.original_pk}-key-{key}-cell"
        cached = cache.get(cache_key)
        if cached:
            return cached
        for line in self.structure:
            for cell in line:
                if cell.cell_name == key:
                    cache.set(cache_key, cell)
                    return cell
        return None

    def get_cell_content(self, raw_input: str) -> MetaFilterWidgetElement:
        parts = raw_input.split(".")
        if parts.__len__() < 3:
            raise Exception(f"Cell content not parseable: {raw_input}")
        cell_type = parts[0]
        cell_name = parts[1]
        cell_func = parts[2]
        cell_arg = parts[3] if parts.__len__() > 4 else None
        cell_obj = MetaFilterWidgetElement(cell_type, cell_name, cell_func, cell_arg)
        cell_obj.verify()
        return cell_obj


class MetaFilterWidget(Widget):
    # To keep this simple, this is for now one field instead of an additional nested structure
    structure = models.TextField(default=None, null=True, blank=True)

    @property
    def parsed_structure(self) -> MetaFilterWidgetStructure | None:
        cache_key = f"metafilterwidget-parsed-structure-{self.pk}"
        cached = cache.get(cache_key)
        if cached:
            return cached
        if not self.structure:
            return None
        structure = list(loads(self.structure))
        obj = MetaFilterWidgetStructure(structure, self.pk)
        obj.parse()
        cache.set(cache_key, obj)
        return obj

    def get_assignments_for_meta_values(
        self,
        meta_filter_values,
        choosable: Choosable,
        collected_assignments: Dict[int, List[FacetteAssignment]],
        session: Session,
    ) -> FacetteAssignment | None:
        """
        Get a FacetteAssignment caused by a given choosable by a given meta        
        """
        structure = self.parsed_structure
        if not structure:
            return None
        
        for stored_value in meta_filter_values:
            cell_obj = structure.get_cell_from_structure(stored_value.key)
            if cell_obj:
                stored_value_value = stored_value.value

                result = cell_obj.apply_cell_func(
                    choosable, stored_value_value, collected_assignments, session
                )
                if result:
                    return result
        return None


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
    page = models.ForeignKey(
        to=Page,
        on_delete=models.CASCADE,
        blank=True,
        default=None,
        null=True,
        related_name="meta_filter_value_page",
    )
