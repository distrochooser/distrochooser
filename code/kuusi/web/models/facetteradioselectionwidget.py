"""
kuusi
Copyright (C) 2014-2023  Christoph Müller <mail@chmr.eu>

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

from typing import Tuple, Dict, List
from web.models import Facette, Session, FacetteSelectionWidget, FacetteSelection, WebHttpRequest, Page
from web.forms import WarningForm
from logging import getLogger
from django import forms
from django.forms import Form
from django.template import loader

logger = getLogger("root");

class FacetteRadioSelectionWidget(FacetteSelectionWidget):
    NOTHING_SELECTED = "nothing";
    def build_form(
        self, data: Dict | None, session: Session
    ) -> Tuple[WarningForm, List, Dict]:
        facette_form = WarningForm(data) if data else WarningForm()
        facettes = None
        if session.valid_for == "latest":
            facettes = Facette.objects.filter(topic=self.topic, is_invalidated=False)
        else:
            logger.debug(f"Facette radio widget {self} will use facettes of invalidation {session.valid_for}.")
            facettes = Facette.objects.filter(topic=self.topic, is_invalidated=True, invalidation_id=session.valid_for)
        child_facettes = []
        weights = {}
        # TODO: Implement child facette selection (maybe?)
        # TODO: Inject language here to the __() call
        # Build the form content
        names = []
        names.append((FacetteRadioSelectionWidget.NOTHING_SELECTED, FacetteRadioSelectionWidget.NOTHING_SELECTED))
        default_selection = FacetteRadioSelectionWidget.NOTHING_SELECTED
        facette: Facette
        for facette in facettes:
            names.append((facette.catalogue_id, facette.__("selectable_description", "en")))

            selection_matches = FacetteSelection.objects.filter(
                    facette=facette, session=session
            )
            is_selected = (
                selection_matches.count()
                > 0
            )

            if is_selected:
                weights[self.topic] = selection_matches.first().weight
                default_selection = facette.catalogue_id
            
        radio_group = forms.CharField(widget=forms.RadioSelect(choices=names, attrs={
            "data-ku-facette": self.topic
        }))

        facette_form.fields[self.topic] = radio_group
        facette_form.initial[self.topic] = default_selection
        return facette_form, child_facettes, weights

    def proceed(self, request: WebHttpRequest, page: Page) -> bool:
        # Always remove the facettes for the current widget to prevent permanent selections
        if request.method == "POST":
            active_facette = request.POST.get(self.topic)
            if active_facette != FacetteRadioSelectionWidget.NOTHING_SELECTED:
                weight = request.POST.get(f"{self.topic}-weight")
                if active_facette:
                    FacetteSelection.objects.filter(
                        session=request.session_obj, facette__topic=self.topic
                    ).delete()
                    facette = None
                    if request.session_obj.valid_for == "latest":
                        facette = Facette.objects.get(topic=self.topic, is_invalidated=False, catalogue_id=active_facette)
                        logger.debug(f"Facette radio widget {self} will use facette of current invalidation {request.session_obj.valid_for} for selection.")
                    else:
                        logger.debug(f"Facette radio widget {self} will use facette of invalidation {request.session_obj.valid_for} for selection.")
                        facette = facette=Facette.objects.get(topic=self.topic, is_invalidated=True, catalogue_id=active_facette, invalidation_id=request.session_obj.valid_for)
                    select = FacetteSelection(facette=facette, session=request.session_obj)
                    select.weight = weight
                    select.save()
        
        facette_form, _ , _= self.build_form(request.POST, request.session_obj)
        # TODO: Add behaviours for Radio selections
        request.has_warnings = facette_form.has_warning()
        request.has_errors = not facette_form.is_valid()
        if request.has_warnings or request.has_errors:
            return False
        return True

    def render(self, request: WebHttpRequest, page: Page):
        render_template = loader.get_template(f"widgets/facette.html")
        data = None
        facette_form = Form()
        if request.method == "POST":
            data = request.POST
        else:
            data = {}
            selected_facettes = FacetteSelection.objects.filter(
                session=request.session_obj
            ).filter(facette__topic=self.topic)

            selection: Facette
            for selection in selected_facettes:
                data[self.topic] = selection.facette.catalogue_id
        facette_form, child_facettes, weights = self.build_form(data, request.session_obj)
        context = {}
        context["form"] = facette_form

        return render_template.render(
            {"form": facette_form, "child_facettes": child_facettes, "weights": weights}, request
        )
