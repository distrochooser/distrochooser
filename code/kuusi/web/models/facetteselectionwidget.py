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
from web.models import Session, Widget, FacetteSelection, FacetteBehaviour, Page, PageMarking, WebHttpRequest
from web.forms import WarningForm
from django.template import loader
from django.utils.safestring import mark_safe
from django.forms import Form, BooleanField
from django.db.models import Q

from logging import getLogger

logger = getLogger("root")

class FacetteSelectionWidget(Widget):
    topic = models.CharField(null=False, blank=False, max_length=120)
    # FIXME: The description field will not be taken over by any i18n processes, Translateablefield is not really available as FacetteSelectionWidget inherits Widget, not Translateable
    description = models.TextField(null=True, blank=True, default=None, max_length=250)
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
        selections = FacetteSelection.objects.filter(session=session)
        active_facettes = []

        selection: FacetteSelection
        for selection in selections:
            if selection.facette not in active_facettes:
                active_facettes.append(selection.facette)
        # FIXME: Facettes not triggering
        facette: Facette
        for facette in active_facettes:
            behaviours = FacetteBehaviour.objects.filter(
                Q(affected_subjects__pk__in=[facette.pk])|
                Q(affected_objects__pk__in=[facette.pk])
            )
            # We only care about behavours true for a facette within the current screen while we iterate all facettes *somewhere* selected
            not_this = list(
                filter(lambda f: f.pk != facette.pk, active_facettes_this_widget)
            )
            behaviour: FacetteBehaviour
            for behaviour in behaviours:
                result = behaviour.is_true(facette, not_this)
                if result:
                    if behaviour.criticality == FacetteBehaviour.Criticality.ERROR:
                        facette_form.add_error(
                            facette.catalogue_id, behaviour.description
                        )
                    elif behaviour.criticality == FacetteBehaviour.Criticality.WARNING:
                        facette_form.add_warning(
                            facette.catalogue_id, behaviour.description
                        )
                    else:
                        # TODO: Implement facette behaviour for criticality INFO
                        pass
        # FIXME: Facettes do not display the behaviour
        # Log a warning as this might cause headache later
        if facette_form.errors.__len__() > 0 or facette_form.warnings.__len__() > 0:
            if self.pages.count() > 0:
                logger.warn(f"There will be markings due to errors/ warnings in widget {self} for more than one page.")
        page: Page
        for page in self.pages.all():
            PageMarking.objects.filter(session=session, page=page).filter(Q(is_error=True)|Q(is_warning=True)).delete()
            if facette_form.errors.__len__() > 0 or facette_form.warnings.__len__() > 0:
                # Create a non-deletable Marking for pages using this widget
                # In case of facette selection widgets, this will most likely be one.
                marking = PageMarking(
                    session=session,
                    page=page,
                    is_error = facette_form.errors.__len__() > 0,
                    is_warning = facette_form.warnings.__len__() > 0
                )
                marking.save()

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
        # TODO: Make more dependend from the page rather than the topic
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
                data[selection.facette.catalogue_id] = "on"
        facette_form, child_facettes, weights = self.build_form(data, request.session_obj)
        context = {}
        context["form"] = facette_form

        return render_template.render(
            {"language_code": request.session_obj.language_code, "form": facette_form, "child_facettes": child_facettes, "weights": weights}, request
        )