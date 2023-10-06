"""
kuusi
Copyright (C) 2015-2023  Christoph Müller <mail@chmr.eu>

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

from __future__ import annotations
from typing import Any, List, Dict, Tuple
from os.path import join, exists
from os import mkdir, listdir
from logging import getLogger

from django import forms
from django.db import models
from django.db.models import Max, Min, QuerySet
from django.template import loader
from django.utils import timezone

from django.http import HttpRequest

from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.forms import Form, BooleanField
from django.utils.safestring import mark_safe

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext as _

import random
import string
from polib import pofile

from kuusi.settings import (
    LOCALE_PATHS,
    LANGUAGES,
    BASE_DIR,
    KUUSI_URL,
    SESSION_NUMBER_OFFSET,
    WEIGHT_MAP
)
from web.forms import WarningForm

logger = getLogger("root")


class WebHttpRequest(HttpRequest):
    session_obj: Session = None
    has_warnings: bool = False
    has_errors: bool = False


class TranslateableField(models.CharField):
    "A field which can be translated"

    def __init__(self, *args, **kwargs):
        kwargs["help_text"] = "A comment for translators to identify this value"
        super().__init__(*args, **kwargs)

    def get_msg_id(self, model_instance: Translateable):
        """
        Get a unique identifier to be used for translation purposes.
        """
        model_type = type(model_instance).__name__
        identifier = model_instance.pk
        if model_instance.catalogue_id:
            identifier = model_instance.catalogue_id
        return f"{model_type}_{identifier}_{self.name}".upper()

    def get_po_block(self, model_instance: Translateable):
        """
        Return the block to be written into the PO file.
        A msg_str might be appended if an translation is existing within the locale context.
        """
        comment = self.value_from_object(model_instance)
        name = self.name
        model_type = type(model_instance).__name__
        pk = model_instance.pk
        msg_id = self.get_msg_id(model_instance)
        return f'\n# Model reference: {model_type}.{pk}\n# Attribute name: {name}, remark: {comment}\nmsgid "{msg_id}"'

    def pre_save(self, model_instance: Translateable, add: bool) -> Any:
        """
        Update records to make sure there is a record existing at all the time
        """
        if len(LOCALE_PATHS) == 0:
            raise Exception(f"No locale paths are set")

        # Make sure that the TranslateAbleField has a record we can reference
        TranslateableFieldRecord.objects.filter(
            msg_id=self.get_msg_id(model_instance)
        ).delete()
        record = TranslateableFieldRecord.objects.create(
            msg_id=self.get_msg_id(model_instance),
            po_block=self.get_po_block(model_instance),
        )

        logger.debug(f"TranslatableFieldRecord is {record}")
        model_instance.update_po_file()
        return super().pre_save(model_instance, add)


class TranslateableFieldRecord(models.Model):
    msg_id = models.CharField(null=False, blank=False, max_length=50)
    po_block = models.TextField(null=True, blank=True, max_length=1000)

    def __str__(self) -> str:
        return self.msg_id


class Translateable(models.Model):
    """
    This class is just used to trigger a signal, which clears up unused TranslateableFieldRecords

    If a TranslateField shall be used, the model must inherit this class.
    """

    catalogue_id = models.CharField(null=True, blank=True, default=None, max_length=20)

    is_invalidated = models.BooleanField(default=False)
    invalidation_id = models.CharField(max_length=5, default=None,null=True,blank=True)

    def __(self, key: str, language_code: str = "en") -> str:
        msg_id = self._meta.get_field(key).get_msg_id(self)
        # TODO: make this block in a function
        # TODO: make this in memory
        translation_path = join(
            LOCALE_PATHS[0], language_code, "LC_MESSAGES", "translateable.po"
        )
        existing_record_translations = {}
        if exists(translation_path):
            po = pofile(translation_path)
            for entry in po:
                existing_record_translations[entry.msgid] = entry.msgstr
        if (
            msg_id not in existing_record_translations
            or len(existing_record_translations[msg_id]) == 0
        ):
            return msg_id
        return existing_record_translations[msg_id]

    def remove_translation_records(self):
        """
        Removes the translation records form the database.
        """
        fields = self._meta.get_fields()

        field: models.Field | TranslateableField
        for field in fields:
            field_type = type(field)
            field_name = field.name
            if isinstance(field, TranslateableField):
                logger.debug(f"Removing field records for {field_type} ({field_name})")
                TranslateableFieldRecord.objects.filter(
                    msg_id=field.get_msg_id(self)
                ).delete()

    def update_po_file(self):
        """
        Update the PO file to represent the currently used records
        """
        for lang in LANGUAGES:
            key = lang[0]
            if not exists(join(LOCALE_PATHS[0], key)):
                mkdir(join(LOCALE_PATHS[0], key))
            if not exists(join(LOCALE_PATHS[0], key, "LC_MESSAGES")):
                mkdir(join(LOCALE_PATHS[0], key, "LC_MESSAGES"))

            translation_path = join(
                LOCALE_PATHS[0], key, "LC_MESSAGES", "translateable.po"
            )
            existing_record_translations = {}
            if exists(translation_path):
                po = pofile(translation_path)
                for entry in po:
                    existing_record_translations[entry.msgid] = entry.msgstr

            # write the PO file
            all_records = TranslateableFieldRecord.objects.all().order_by("-msg_id")
            with open(translation_path, "w") as file:
                record: TranslateableFieldRecord
                for record in all_records:
                    msg_str = ""
                    if record.msg_id in existing_record_translations:
                        msg_str = existing_record_translations[record.msg_id]
                    file.write(record.po_block + f'\nmsgstr "{msg_str}"')


@receiver(pre_delete, sender=Translateable)
def translateable_removing(sender, instance, using, **kwargs):
    origin: Translateable | models.QuerySet = kwargs["origin"]
    if isinstance(origin, models.QuerySet):
        entry: Translateable
        for entry in origin:
            entry.remove_translation_records()
            entry.update_po_file()
    else:
        origin.remove_translation_records()
        origin.update_po_file()


class Page(Translateable):
    title = TranslateableField(null=False, blank=False, max_length=120)
    next_page = models.ForeignKey(
        to="Page",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
        related_name="page_next",
    )
    require_session = models.BooleanField(default=False)
    not_in_versions = models.ManyToManyField(to="SessionVersion", blank=True)
    can_be_marked = models.BooleanField(default=False)
    no_header = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.title}"

    @property
    def href(self):
        return f"/?page={self.catalogue_id}"

    def is_visible(self, session: Session | None) -> bool:
        """
        Returns if the page is visible in view of the session version
        """
        is_page_visible = True
        if session and session.version:
            if self.not_in_versions.filter(pk=session.version.pk).count() > 0:
                is_page_visible = False
        return is_page_visible

    @property
    def previous_page(self) -> Page | None:
        return Page.objects.filter(next_page=self).first()

    @property
    def widget_list(self) -> List[Widget]:
        # NavigationWidgets are the last set of widgets as they might need to know if errors appeared before.
        return (
            list(SessionVersionWidget.objects.filter(pages__pk__in=[self]))
            + list(HTMLWidget.objects.filter(pages__pk__in=[self]))
            + list(FacetteSelectionWidget.objects.filter(pages__pk__in=[self]))
            + list(ResultListWidget.objects.filter(pages__pk__in=[self]))
            + list(ResultShareWidget.objects.filter(pages__pk__in=[self]))
            + list(NavigationWidget.objects.filter(pages__pk__in=[self]))
        )

    def proceed(self, request: WebHttpRequest) -> bool:
        for widget in self.widget_list:
            result = widget.proceed(request, self)
            if not result:
                return False

        return True

    @property
    def facette_selections(self) -> List[FacetteSelectionWidget]:
        widgets_used = FacetteSelectionWidget.objects.filter(pages__pk__in=[self])
        return widgets_used

    @property
    def facette_selection_descriptions(self) -> List[str]:
        """
        Return a list of descriptions collected within FacetteSelectionWidgets of this page
        """
        result = list()
        widgets_used = self.facette_selections
        widget: FacetteSelectionWidget
        for widget in widgets_used:
            if widget.description:
                result.append(widget.description)

        return result

    @property
    def facette_selection_topics(self) -> List[str]:
        """
        Return a list of topics collected within FacetteSelectionWidgets of this page
        """
        result = list()
        widgets_used = self.facette_selections
        widget: FacetteSelectionWidget
        for widget in widgets_used:
            if widget.topic:
                result.append(widget.topic)

        return result

    @property
    def structure(self) -> List[List[Widget]]:
        """
        Returns the structure of the page as a 2-dimensional list containing widgets.

        X and Y are hereby the cols to be used.
        """
        result = list()
        widgets_used = self.widget_list
        all_widgets = Widget.objects.filter(pages__in=[self])
        max_row = all_widgets.aggregate(Max("row"))["row__max"]
        max_col = all_widgets.aggregate(Max("col"))["col__max"]
        min_row = all_widgets.aggregate(Min("row"))["row__min"]
        min_col = all_widgets.aggregate(Min("col"))["col__min"]
        if not max_row or not max_col:
            logger.debug(f"The page {self} has no widgets")
            return result
        logger.debug(
            f"The page {self} spans as follows {min_col},{min_row} -> {max_col}, {max_row}"
        )
        for y in range(min_row, max_row + 1):
            row_list = list()
            for x in range(min_col, max_col + 1):
                matches = list(
                    filter(lambda w: w.col == x and w.row == y, widgets_used)
                )
                widget = matches[0] if len(matches) > 0 else None
                if widget:
                    row_list.append(widget)
                else:
                    row_list.append(None)
            result.append(row_list)
        logger.debug(result)
        return result

    def is_marked(self, session: Session):
        return PageMarking.objects.filter(page=self, session=session).count() > 0

    def toggle_marking(self, session: Session):
        marking_matches = PageMarking.objects.filter(page=self, session=session)

        if marking_matches.count() > 0:
            marking_matches.delete()
        else:
            marking = PageMarking(page=self, session=session)
            marking.save()


class PageMarking(models.Model):
    page = models.ForeignKey(
        to=Page,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="pagemarking_page",
    )
    session = models.ForeignKey(
        to="Session",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="pagemarking_session",
    )


class Widget(models.Model):
    row = models.IntegerField(default=1, null=False, blank=False)
    col = models.IntegerField(default=1, null=False, blank=False)
    width = models.IntegerField(default=1, null=False, blank=False)
    pages = models.ManyToManyField(to=Page, blank=True, default=None)

    def render(self, request: HttpRequest, page: Page):
        raise Exception()

    def proceed(self, request: HttpRequest, page: Page) -> bool:
        raise Exception()


class HTMLWidget(Widget):
    template = models.CharField(null=False, blank=False, max_length=25)

    def __init__(self, *args, **kwargs):
        template_path = join(BASE_DIR, "web", "templates", "widgets")
        raw_templates = listdir(template_path)
        templates = []
        for template in raw_templates:
            templates.append((template, template))
        self._meta.get_field("template").choices = templates
        self._meta.get_field("template").widget = forms.Select(choices=templates)
        super(HTMLWidget, self).__init__(*args, **kwargs)

    def __str__(self) -> str:
        return self.template

    def render(self, request: HttpRequest, page: Page):
        render_template = loader.get_template(f"widgets/{self.template}")
        return render_template.render({}, request)

    def proceed(self, request: HttpRequest, page: Page) -> bool:
        return True

class FacetteSelectionWidget(Widget):
    topic = models.CharField(null=False, blank=False, max_length=120)
    # FIXME: The description field will not be taken over by any i18n processes, Translateablefield is not really available as FacetteSelectionWidget inherits Widget, not Translateable
    description = models.TextField(null=True, blank=True, default=None, max_length=250)
    def build_translateable_label(self, facette: Facette) -> str:
        render_template = loader.get_template(f"widgets/facette_label.html")
        return mark_safe(render_template.render({
            "title": facette.catalogue_id
        }))
    def build_form(
        self, data: Dict | None, session: Session
    ) -> Tuple[WarningForm, List, Dict]:
        facette_form = WarningForm(data) if data else WarningForm()
        facettes = Facette.objects.filter(topic=self.topic, is_invalidated=False)
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
                facette_form.fields[facette.catalogue_id] = BooleanField(required=False, label=self.build_translateable_label(facette))

                if has_child:
                    attr_map = {
                        "data-bs-toggle": "collapse",
                        "data-bs-target": f"#collapse-{facette.catalogue_id}",
                        "aria-expanded": ("false" if not is_selected else "true"),
                        "aria-controls": f"collapse-{facette.catalogue_id}",
                        "data-ku-id": facette.catalogue_id
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

        # trigger facette behaviours
        # While we need to now _all_ selected facettes, it's also required to know the facettes within the current screen
        active_facettes_this_widget = self.get_active_facettes(facette_form, session)
        selections = FacetteSelection.objects.filter(session=session)
        active_facettes = []

        selection: FacetteSelection
        for selection in selections:
            if selection.facette not in active_facettes:
                active_facettes.append(selection.facette)
        facette: Facette
        for facette in active_facettes:
            behaviours = FacetteBehaviour.objects.filter(is_invalidated=False)
            behaviour: FacetteBehaviour
            for behaviour in behaviours:
                # We only care about behavours true for a facette within the current screen while we iterate all facettes *somewhere* selected
                not_this = list(
                    filter(lambda f: f.pk != facette.pk, active_facettes_this_widget)
                )
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
            {"form": facette_form, "child_facettes": child_facettes, "weights": weights}, request
        )


class NavigationWidget(Widget):
    def proceed(self, request: WebHttpRequest, page: Page) -> bool:
        return True

    def render(self, request: WebHttpRequest, page: Page):
        render_template = loader.get_template(f"widgets/navigation.html")
        return render_template.render(
            {
                "page": page,
                "has_errors": request.has_errors,
                "has_warnings": request.has_warnings,
                "is_marked": page.is_marked(request.session_obj),
            },
            request,
        )


class ResultShareWidget(Widget):
    def proceed(self, request: WebHttpRequest, page: Page) -> bool:
        return True

    def render(self, request: WebHttpRequest, page: Page):
        render_template = loader.get_template(f"widgets/result_share.html")
        return render_template.render(
            {
                "session": request.session_obj,
                "page": page,
                "share_link": f"{KUUSI_URL}/{request.session_obj.result_id}",
            },
            request,
        )


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
                facettes__pk__in=[facette.pk],
                is_invalidated=False
            )
            if assignments.count() > 0:
                assignments_selected += assignments

            # The weight from the selection will be used to alter the score later.
            weights_per_assignment.append(selection.weight)

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
            # FIXME: SOmething causes the get_score() result to be 0 even with negative assignments
            assignments_used[choosable] = []
            assignment: FacetteAssignment
            for assignment in choosable_assignments:
                original_index = assignments_selected.index(assignment)
                weights_this_assignment = weights_per_assignment[original_index]
                weighted_score = 1 * WEIGHT_MAP[weights_this_assignment]
                # TODO: Handle the case that an assignment is used twice?
                logger.debug(f"The assignment {assignment} has weight {weights_this_assignment}, according to it's source selection. The score will be {weighted_score}. The score type is {assignment.assignment_type}")
                results[assignment.assignment_type] += weighted_score

                assignments_used[choosable].append(assignment)

            score = FacetteAssignment.AssignmentType.get_score(results)
            logger.debug(f"Choosable={choosable}, Score={score}, Results={results}")

            raw_results[choosable] = score
        # FIXME: ADd proper sorting.
        ranked_keys = raw_results
        ranked_result = {}
        for key in ranked_keys:
            ranked_result[key] = {
                "choosable": key,
                "score": raw_results[key],
                "assignments": assignments_used[key],
            }

        return render_template.render({"page": page, "results": ranked_result}, request)

def random_str():
    letters = string.ascii_lowercase + "1234567890"
    result_str = "".join(random.choice(letters) for i in range(5))
    return result_str

def get_session_result_id():
    result_str = random_str()
    is_existing = Session.objects.filter(result_id=result_str).count() != 0
    while is_existing:
        result_str = random_str()
        is_existing = Session.objects.filter(result_id=result_str).count() != 0
    return "d6" + result_str


def get_session_number():
    return SESSION_NUMBER_OFFSET + Session.objects.all().count() + 1


class Session(models.Model):
    started = models.DateTimeField(default=timezone.now, null=False, blank=False)
    user_agent = models.CharField(default=None, null=True, blank=True, max_length=150)
    result_id = models.CharField(
        default=get_session_result_id, max_length=10, null=False, blank=False
    )
    version = models.ForeignKey(
        to="SessionVersion",
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        blank=True,
        related_name="session_version",
    )
    number = models.IntegerField(default=get_session_number, null=True, blank=True)
    session_origin = models.ForeignKey(
        to="Session",
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        blank=True,
        related_name="session_sessionorigin",
    )

    # TODO: Add a counter for statistical purposes
    # TODO: Add a flag to define a version on the facette structure to allow to differentiate between database iterations
    @property
    def answered_pages(self):
        pages = Page.objects.all()
        answer_state = {}
        page: Page
        for page in pages:
            # TODO: Make this more variable if an answer could result in a text field value, for example.
            facette_widgets = FacetteSelectionWidget.objects.filter(
                pages__pk__in=[page.pk]
            )
            if facette_widgets.count() > 0:
                widget: FacetteSelectionWidget
                for widget in facette_widgets:
                    has_selections = (
                        FacetteSelection.objects.filter(
                            session=self, facette__topic=widget.topic
                        ).count()
                        > 0
                    )
                    if has_selections:
                        answer_state[page.catalogue_id] = has_selections
        return answer_state


class SessionVersion(Translateable):
    version_name = TranslateableField(null=False, blank=False, max_length=120)


class SessionVersionWidget(Widget):
    def proceed(self, request: WebHttpRequest, page: Page) -> bool:
        # TODO: Force the page to run into an exception if the page afterwards is not requiring a session.

        session = request.session_obj
        version = request.POST.get("KU_SESSION_VERSION")

        if session:
            if version is None or len(version) == 0:
                session.version = None
            else:
                session.version = SessionVersion.objects.get(pk=version)
            session.save()
        return True

    def render(self, request: WebHttpRequest, page: Page):
        render_template = loader.get_template(f"widgets/version.html")
        versions = SessionVersion.objects.filter(is_invalidated=False)
        return render_template.render(
            {
                "versions": versions,
                "selected_version": None
                if not request.session_obj
                else request.session_obj.version,
            },
            request,
        )


class Choosable(Translateable):
    """
    Element ot be choosed.

    Must be translated
    """

    name = TranslateableField(null=False, blank=False, max_length=120)
    description = TranslateableField(
        null=True, blank=True, default=None, max_length=120
    )

    def __str__(self) -> str:
        return f"{self.name}"

    @property
    def meta(self) -> Dict[str, any]:
        meta_objects = ChoosableMeta.objects.filter(meta_choosable=self).order_by(
            "meta_name"
        )
        result = {}
        meta_objects: ChoosableMeta
        for meta_object in meta_objects:
            result[meta_object.meta_name] = meta_object

        return result


class ChoosableMeta(Translateable):
    meta_choosable = models.ForeignKey(
        to=Choosable,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="choosablemeta_choosable",
    )

    class MetaType(models.TextChoices):
        TEXT = "TEXT", "TEXT"
        FLAG = "FLAG", "FLAG"
        LINK = "LINK", "LINK"
        DATE = "DATE", "DATE"

    class MetaName(models.TextChoices):
        CREATED = "CREATED", "CREATED"
        COUNTRY = "COUNTRY", "COUNTRY"
        LICENSES = "LICENSES", "LICENSES"
        WEBSITE = "WEBSITE", "WEBSITE"

    meta_type = models.CharField(
        max_length=20, choices=MetaType.choices, default=MetaType.TEXT
    )
    meta_title = TranslateableField(null=True, blank=True, max_length=120)
    meta_name = models.CharField(
        max_length=25,
        blank=False,
        null=False,
        choices=MetaName.choices,
        default=MetaName.CREATED,
    )
    meta_value = models.CharField(
        max_length=255, blank=False, null=False, default="A value"
    )

    def __str__(self) -> str:
        return f"{self.meta_choosable}: {self.meta_name} ({self.meta_type}) -> {self.meta_value}"


class Facette(Translateable):
    """
    A facette describes a fact narrowing down the selection for choosables.

    The description will be used for displaying results

    The selectable_description is displayed for selection within a page

    The topic reduces a facette to a certain subarea, e. g. "licenses" for Linux distributions
    """

    description = TranslateableField(null=False, blank=False, max_length=120)
    selectable_description = TranslateableField(null=False, blank=False, max_length=120)
    topic = TranslateableField(null=False, blank=False, max_length=120)
    child_facettes = models.ManyToManyField(to="Facette", blank=True)

    @property
    def is_child(self) -> bool:
        return Facette.objects.filter(child_facettes__pk__in=[self.pk]).count() > 0

    @property
    def has_child(self) -> bool:
        return self.child_facettes.count() > 0

    def __str__(self) -> str:
        invalidation_prefix = f"Invalidated: ({self.invalidation_id}): " if self.is_invalidated else ""
        return f"{invalidation_prefix}[{self.topic}] (is_child: {self.is_child}, has_child: {self.has_child}) {self.description} (select: {self.selectable_description})"


class FacetteBehaviour(Translateable):
    description = TranslateableField(null=False, blank=False, max_length=120)
    affected_objects = models.ManyToManyField(
        to="Facette", blank=True, related_name="facette_behaviour_objects"
    )
    affected_subjects = models.ManyToManyField(
        to="Facette", blank=True, related_name="facette_behaviour_subjects"
    )

    class Direction(models.TextChoices):
        SUBJECT_TO_OBJECT = "SUBJECT_TO_OBJECT", "SUBJECT_TO_OBJECT"
        OBJECT_TO_SUBJECT = "OBJECT_TO_SUBJECT", "OBJECT_TO_SUBJECT"
        BIDIRECTIONAL = "BIDIRECTIONAL", "BIDIRECTIONAL"
        
    direction = models.CharField(
        max_length=20, choices=Direction.choices, default=Direction.BIDIRECTIONAL
    )

    class Criticality(models.TextChoices):
        WARNING = "WARNING", "WARNING"
        ERROR = "ERROR", "ERROR"
        INFO = "INFO", "INFO"

    criticality = models.CharField(
        max_length=20, choices=Criticality.choices, default=Criticality.ERROR
    )

    def facette_in_queryset(self, facettes: List[Facette], queryset: QuerySet):
        for facette in facettes:
            if queryset.filter(pk=facette.pk).count() > 0:
                return True
        return False

    def is_true(self, facette: Facette, others: List[Facette]) -> bool:
        is_self = self.affected_subjects.filter(pk__in=[facette.pk]).count() > 0
        is_others = self.affected_objects.filter(pk__in=[facette.pk]).count() > 0

        is_subjects_others = self.facette_in_queryset(others, self.affected_subjects)
        is_objects_others = self.facette_in_queryset(others, self.affected_objects)

        if self.direction == FacetteBehaviour.Direction.BIDIRECTIONAL:
            if is_self or is_others:
                return True

        if self.direction == FacetteBehaviour.Direction.SUBJECT_TO_OBJECT:
            if is_self and is_objects_others:
                return True

        if self.direction == FacetteBehaviour.Direction.OBJECT_TO_SUBJECT:
            if is_others and is_subjects_others:
                return True
        return False


class FacetteSelection(models.Model):
    facette = models.ForeignKey(
        to=Facette,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="facetteseletion_facette",
    )
    session = models.ForeignKey(
        to=Session,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="facetteseletion_session",
    )
    weight = models.IntegerField(
        default=0, validators=[MaxValueValidator(2), MinValueValidator(-2)]
    )


class FacetteAssignment(Translateable):
    choosables = models.ManyToManyField(to=Choosable)
    facettes = models.ManyToManyField(to=Facette)
    description = TranslateableField(
        null=True, blank=True, default=None, max_length=255
    )
    long_description = TranslateableField(
        null=True, blank=True, default=None, max_length=800
    )

    @property
    def facette_topics(self) -> List[str]:
        """
        Returns a set of facette objects to return a unique list of topics. The Facette objects are used as translatables to provide the needed __() function
        """
        topics = []
        results = []
        facette: Facette
        for facette in self.facettes.all():
            if facette.topic not in topics:
                topics.append(facette.topic)
                results.append(facette)
        return results

    class AssignmentType(models.TextChoices):
        POSITIVE = "POSITIVE", "POSITIVE"
        NEGATIVE = "NEGATIVE", "NEGATIVE"
        NEUTRAL = "NEUTRAL", "NEUTRAL"

        def get_score(haystack: Dict) -> float:
            """
            Calculate a numeric score for a given result set.

            The result set is keys from this class with numeric values.

            The calculation is located here to allow the assignment types to be extended without altering major parts of the code.
            """
            score_map = {
                FacetteAssignment.AssignmentType.POSITIVE: 1,
                FacetteAssignment.AssignmentType.NEGATIVE: -1,
                FacetteAssignment.AssignmentType.NEUTRAL: 0,
            }
            score = 0
            for key, value in haystack.items():
                score += score_map[key] * value

            return score

    assignment_type = models.CharField(
        max_length=20, choices=AssignmentType.choices, default=AssignmentType.NEUTRAL
    )


class Category(Translateable):
    name = TranslateableField(null=False, blank=False, max_length=120)
    icon = models.CharField(
        null=False, blank=False, default="bi bi-clipboard2-data", max_length=100
    )
    identifier = models.CharField(null=False, blank=False, max_length=100)
    child_of = models.ForeignKey(
        to="Category",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
        related_name="category_child_of",
    )
    target_page = models.ForeignKey(
        to="Page",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
        related_name="category_target_page",
    )

    def to_step(
        self,
        current_location: str,
        language_code: str,
        session: Session | None,
        is_last: bool = False,
    ) -> Dict | None:
        """
        Returns the structure so that the custom tag "steps" can generate the navigation element.

        If the target page is not fitting the version of the session, None is returned.
        """
        target = None
        target_page: Page = self.target_page
        if target_page:
            target = target_page.href

            if not target_page.is_visible(session):
                return None
            is_answered = (
                target_page.catalogue_id in session.answered_pages
                if session and target_page.catalogue_id in session.answered_pages
                else False
            )
            is_marked = target_page.is_marked(session)
        return {
            "title": self.__("name", language_code),
            "href": target,
            "active": current_location == target, # FIXME: Properly identify the current location also when /<language>/<id> is set
            "answered": is_answered,
            "marked": is_marked,
            "last": is_last,
        }

    def __str__(self) -> str:
        return f"[{self.icon}] {self.name} -> {self.target_page} (child of: {self.child_of})"


class TranslationSuggestion(models.Model):
    lang_code = models.CharField(max_length=10,blank=False, null=False)
    lang_key = models.CharField(max_length=255,blank=False, null=False)
    lang_value = models.CharField(max_length=255,blank=False, null=False)
    amount = models.IntegerField(default=0, blank=False, null=False)    

    def __str__(self) -> str:
        return f"[{self.lang_code}]: {self.lang_key} = {self.lang_value} ({self.amount}x)"