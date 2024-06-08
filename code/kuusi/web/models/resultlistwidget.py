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
            assignments = FacetteAssignment.objects.filter(
                    facettes__pk__in=[facette.pk]
            )
            
            if assignments.count() > 0:
                assignments_selected += assignments

            # The weight from the selection will be used to alter the score later.
            # Iterate the newly attached assignments ot make sure that cound(weights_per_assignments) == count(assignments_selected)
            for assignment in assignments:
                weights_per_assignment.append(selection.weight)

        choosables = Choosable.objects.all()

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
        all_scores = list(filter(lambda s: s!= 0, set(map(lambda s: s, raw_results.values()))))
        all_scores.sort()
        all_scores.reverse()
        ranked_result = {}
        # TODO: Add weights for display (also on navigation steps!)
        for key in ranked_keys:
            if len(assignments_used[key]) > 0:
                sorted_assignments = sorted(assignments_used[key])
                assignment_stats = {}
                for value in sorted_assignments:
                    assignment = value[0]
                    if assignment.assignment_type not in assignment_stats:
                        assignment_stats[assignment.assignment_type] = 1
                    else: 
                        assignment_stats[assignment.assignment_type]+=1
                ranked_result[key] = {
                    "choosable": key,
                    "score": raw_results[key],
                    "assignments": sorted_assignments,
                    "position": all_scores.index(raw_results[key]) + 1,
                    "stats": assignment_stats
                }
        # Default mode is compact unless the session or the get parameter overwrites it
        display_mode = "compact" if not request.session_obj.display_mode else request.session_obj.display_mode
        if request.GET.get("switch_to") is not None and request.GET.get("switch_to") in ["list", "compact"]:
            display_mode = request.GET.get("switch_to")
            request.session_obj.display_mode = display_mode
            request.session_obj.save()
        return render_template.render({"display_mode": display_mode, "page": page, "results": ranked_result}, request)
