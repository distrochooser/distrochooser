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

from typing import Dict
from web.models import Widget, WebHttpRequest, Page, FacetteSelection, FacetteAssignment, Choosable
from django.template import loader

from kuusi.settings import WEIGHT_MAP

from logging import getLogger

logger = getLogger("root")

class ResultListWidget(Widget):
    def proceed(self, request: WebHttpRequest, page: Page) -> bool:
        return True

    def render(self, request: WebHttpRequest, page: Page):
        render_template = loader.get_template(f"widgets/result_list.html")
        selections = FacetteSelection.objects.filter(session=request.session_obj)

        assignments_selected = list()
        weights_per_assignment = list()


        selection: FacetteSelection
        for selection in selections:
            facette = selection.facette
            assignments = None
            if request.session_obj.valid_for != "latest":
                logger.debug(f"The session is not for latest, choosing assignments of invalidation {request.session_obj.valid_for}.")
                assignments = FacetteAssignment.objects.filter(
                    facettes__pk__in=[facette.pk],
                    is_invalidated=True,
                    invalidation_id=request.session_obj.valid_for
                )
            else:
                assignments = FacetteAssignment.objects.filter(
                    facettes__pk__in=[facette.pk],
                    is_invalidated=False
                )
            
            if assignments.count() > 0:
                assignments_selected += assignments

            # The weight from the selection will be used to alter the score later.
            # Iterate the newly attached assignments ot make sure that cound(weights_per_assignments) == count(assignments_selected)
            for assignment in assignments:
                weights_per_assignment.append(selection.weight)

        choosables = None
        if request.session_obj.valid_for != "latest":
            logger.debug(f"The session is not for latest, choosing choosables of invalidation {request.session_obj.valid_for}.")
            choosables = Choosable.objects.filter(invalidation_id=request.session_obj.valid_for, is_invalidated=True)
        else:
            choosables = Choosable.objects.filter(is_invalidated=False)

        raw_results: Dict[Choosable, float] = {}
        assignments_used: Dict[Choosable, FacetteAssignment] = {}
        choosable: Choosable
        for choosable in choosables:
            # TODO: This must be done EASIER FFS
            assignment_types = FacetteAssignment.AssignmentType.__dict__.get(
                "_member_map_"
            )
            results = {}
            for key, _ in assignment_types.items():
                results[key] = 0

            # get facette assingments actually relevant for this choosable
            choosable_assignments = list(
                filter(
                    lambda a: a.choosables.filter(pk=choosable.pk).count() == 1,
                    assignments_selected,
                )
            )
            assignments_used[choosable] = []
            assignment: FacetteAssignment
            for assignment in choosable_assignments:
                original_index = assignments_selected.index(assignment)
                weights_this_assignment = weights_per_assignment[original_index]
                weighted_score = 1 * WEIGHT_MAP[weights_this_assignment]
                # TODO: Handle the case that an assignment is used twice?
                results[assignment.assignment_type] += weighted_score

                assignments_used[choosable].append((assignment, weighted_score))
            score = FacetteAssignment.AssignmentType.get_score(results)
            logger.debug(f"Choosable={choosable}, Score={score}, Results={results}")
            raw_results[choosable] = score

        ranked_keys =sorted(raw_results, key=raw_results.get, reverse=True)
        ranked_result = {}
        # TODO: Add weights for display (also on navigation steps!)
        for key in ranked_keys:
            ranked_result[key] = {
                "choosable": key,
                "score": raw_results[key],
                "assignments": assignments_used[key],
            }

        return render_template.render({"page": page, "results": ranked_result}, request)
