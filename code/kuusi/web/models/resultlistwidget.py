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
from web.models import Widget, WebHttpRequest, Page, FacetteSelection, FacetteAssignment, Choosable, SessionMeta
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

        active_filters = []
        pre_filters = {
            "RESULT_MORE_THAN_5": lambda c: c.meta["AGE"].years_since >= 5 if "AGE" in c.meta else True,
            "RESULT_MORE_THAN_15": lambda c: c.meta["AGE"].years_since >= 15 if "AGE" in c.meta else True,
            "RESULT_MORE_THAN_20": lambda c: c.meta["AGE"].years_since >= 20 if "AGE" in c.meta else True
        }
        # presect filters
        stored_filter = request.session_obj.get_meta_value("RESULT_AGE_FILTER")
        logger.debug(f"Stored filter is {stored_filter}")

        # User deselects the active filter or switches the filter
        if request.GET.get("disable_filter") == stored_filter or stored_filter != request.GET.get("toggle_filter"):
            SessionMeta.objects.filter(
                session=request.session_obj,
                meta_key = "RESULT_AGE_FILTER"
            ).delete()


        for filter_key, delegate in pre_filters.items():
            filter_enabled = request.GET.get("toggle_filter") == filter_key and not request.GET.get("disable_filter")
            if filter_enabled:
                # create meta object to persist the filter while deleting any other prefilters
                SessionMeta(
                    session=request.session_obj,
                    meta_key = "RESULT_AGE_FILTER",
                    meta_value=filter_key
                ).save()
                
                if filter_key not in active_filters:
                    active_filters.append(filter_key)
                choosables = list(filter(delegate, choosables))

        raw_results: Dict[Choosable, float] = {}
        assignments_used: Dict[Choosable, FacetteAssignment] = {}
        choosable: Choosable
        for choosable in choosables:
            results = {}
            for key in FacetteAssignment.AssignmentType.choices:
                identifier, _ = key
                results[identifier] = 0

            # get facette assingments actually relevant for this choosable
            choosable_assignments = list(
                filter(
                    lambda a: a.choosables.filter(pk=choosable.pk).count() == 1,
                    assignments_selected,
                )
            )
            used_assignment = []
            assignments_used[choosable] = []
            assignment: FacetteAssignment
            for assignment in choosable_assignments:
                # only use this assignment if not already processed in another context (e. g. bidirectional cases)
                if assignment.pk not in used_assignment:
                    original_index = assignments_selected.index(assignment)
                    weights_this_assignment = weights_per_assignment[original_index]
                    weighted_score = 1 * WEIGHT_MAP[weights_this_assignment]
                    results[assignment.assignment_type] += weighted_score

                    assignments_used[choosable].append((assignment, weighted_score))
                    used_assignment.append(assignment.pk)
            score = FacetteAssignment.AssignmentType.get_score(results)
            logger.debug(f"Choosable={choosable}, Score={score}, Results={results}")
            raw_results[choosable] = score

        ranked_keys =sorted(raw_results, key=raw_results.get, reverse=True)
        all_scores = list(filter(lambda s: s!= 0, set(map(lambda s: s, raw_results.values()))))
        all_scores.sort()
        all_scores.reverse()
        ranked_result = {}
        last_position = -1
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
                position = all_scores.index(raw_results[key]) + 1 if raw_results[key] in all_scores else 1
                ranked_result[key] = {
                    "choosable": key,
                    "score": raw_results[key],
                    "assignments": sorted_assignments,
                    "position": position,
                    "stats": assignment_stats,
                    "new_group": last_position != position
                }
                last_position = ranked_result[key]["position"]
        # Default mode is compact unless the session or the get parameter overwrites it
        display_mode = "compact" if not request.session_obj.display_mode else request.session_obj.display_mode
        if request.GET.get("switch_to") is not None and request.GET.get("switch_to") in ["list", "compact"]:
            display_mode = request.GET.get("switch_to")
            request.session_obj.display_mode = display_mode

        return render_template.render({ "result_id": request.session_obj.result_id, "language_code": request.session_obj.language_code, "feedback_given": request.GET.get("feedback") is not None, "active_filters": active_filters, "filters": pre_filters, "display_mode": display_mode, "page": page, "results": ranked_result}, request)
