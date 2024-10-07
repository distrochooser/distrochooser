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

from typing import Tuple, Dict, List
from django.db import models
from web.models import Facette
from web.models import Session, Widget, FacetteSelection, Page, WebHttpRequest
from web.forms import WarningForm
from django.template import loader
from django.forms import Form, BooleanField
from web.helper import trigger_behaviours, get_active_facettes

from logging import getLogger

logger = getLogger("root")

class FacetteSelectionWidget(Widget):
    topic = models.CharField(null=False, blank=False, max_length=120)
    def build_translateable_label(self, facette: Facette, language_code: str) -> str:
        return  facette.__("selectable_description", language_code)
    def build_form(
        self, data: Dict | None, session: Session
    ) -> Tuple[WarningForm, List, Dict]:
        facette_form = WarningForm(data) if data else WarningForm()

        facettes = Facette.objects.filter(topic=self.topic)
        child_facettes = []
        weights = {}

        # Build the form content
        facette: Facette
        for facette in facettes:
            is_child = facette.is_child
            has_child = facette.has_child
            selection_matches = FacetteSelection.objects.filter(
                    facette=facette, session=session
            )
            is_selected = (
                selection_matches.count()
                > 0
            )

            if is_selected:
                weights[facette.catalogue_id] = selection_matches.first().weight
            if not is_child:
                facette_form.fields[facette.catalogue_id] = BooleanField(required=False, label=self.build_translateable_label(facette, session.language_code))
                if has_child:
                    attr_map = {
                        "data-bs-toggle": "collapse",
                        "data-bs-target": f"#collapse-{facette.catalogue_id}",
                        "aria-expanded": ("false" if not is_selected else "true"),
                        "aria-controls": f"collapse-{facette.catalogue_id}"
                    }
                    for key, value in attr_map.items():
                        facette_form.fields[facette.catalogue_id].widget.attrs[
                          key
                        ] = value

            for sub_facette in facette.child_facettes.all():
                facette_form.fields[sub_facette.catalogue_id] = BooleanField(
                    required=False,
                    label=self.build_translateable_label(sub_facette)
                )
                facette_form.fields[sub_facette.catalogue_id].widget.attrs[
                    "data-ku-parent"
                ] = facette.catalogue_id
                child_facettes.append(sub_facette.catalogue_id)
            # To make grabbing the facette inputs with selectors for facette.js easier-> add a static attribute
            facette_form.fields[facette.catalogue_id].widget.attrs["data-ku-facette"] = True
            facette_form.fields[facette.catalogue_id].widget.attrs["data-ku-id"] = facette.catalogue_id
        # trigger facette behaviours
        # While we need to now _all_ selected facettes, it's also required to know the facettes within the current screen
        active_facettes_this_widget = self.get_active_facettes(facette_form, session)
        
        active_facettes = get_active_facettes(session)
        
        trigger_behaviours(facette_form, active_facettes, active_facettes_this_widget, session, self.pages)

        return facette_form, child_facettes, weights

    def get_active_facettes(self, form: Form, session: Session) -> List:
        """
        Returns the currently active facettes from the submitted form.
        """
        facettes = Facette.objects.filter(is_invalidated=False)
        active_facettes = []
        if not form.is_valid():
            return active_facettes
        # get selected facettes
        facette: Facette
        for facette in facettes:
            key = facette.catalogue_id
            active = form.cleaned_data.get(key)
            if active:
                active_facettes.append(facette)
        return active_facettes
    def get_active_facettes_raw(self, request: WebHttpRequest, session: Session) -> List:
        """
        Similar as get_active_facettes, but reads from POST directly instead from a given form.
        """
        facettes = Facette.objects.filter(is_invalidated=False)
        active_facettes = []
        # get selected facettes
        facette: Facette
        for facette in facettes:
            key = facette.catalogue_id
            active = request.POST.get(key)
            if active:
                active_facettes.append(facette)
        return active_facettes

    def proceed(self, request: WebHttpRequest, page: Page) -> bool:
        # Always remove the facettes for the current widget to prevent permanent selections
        FacetteSelection.objects.filter(
            session=request.session_obj, facette__topic=self.topic
        ).delete()
        # Get the posted facettes directly from the request to store new selections (including weights)
        active_facettes = self.get_active_facettes_raw(
            request, request.session_obj
        )
        facette: Facette
        for facette in active_facettes:
            weight = 0
            if f"{facette.catalogue_id}-weight" in request.POST:
                raw_weight =request.POST.get(f"{facette.catalogue_id}-weight")

                is_valid_number = raw_weight.isdigit()
                if is_valid_number: # positive values
                    weight = int(raw_weight)
                if "-" in raw_weight: # negative values
                    weight = int(raw_weight[1:]) * -1
                if weight != 0:
                    logger.debug(f"Facette {facette.catalogue_id} will be weighted with {weight}")
                else:
                    logger.debug(f"The string {raw_weight} for field {facette.catalogue_id} could not be casted into an int")

            select = FacetteSelection(facette=facette, session=request.session_obj)
            select.weight = weight
            select.save()
        
        facette_form, _ , _= self.build_form(request.POST, request.session_obj)
        # Make sure there is no double facette selections within this topic of the page
        request.has_errors = facette_form.has_any_behaviour()
        if request.has_errors:
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
                data[selection.facette.catalogue_id] = "on"
        facette_form, child_facettes, weights = self.build_form(data, request.session_obj)
        context = {}
        context["form"] = facette_form

        return render_template.render(
            {"language_code": request.session_obj.language_code, "form": facette_form, "child_facettes": child_facettes, "weights": weights}, request
        )