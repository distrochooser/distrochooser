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

from __future__ import annotations
from django.db import models
from django.db.models import Max, Min
from web.models import SessionVersionWidget, Translateable, TranslateableField, Session, WebHttpRequest, Widget, Facette, FacetteSelection
from typing import List
from logging import getLogger

from django.apps import apps
logger = getLogger("root")

class Page(Translateable):
    next_page = models.ForeignKey(
        to="Page",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
        related_name="page_next",
    )
    not_in_versions = models.ManyToManyField(to="SessionVersion", blank=True)
    can_be_marked = models.BooleanField(default=False)
    hide_text = models.BooleanField(default=False)
    hide_help = models.BooleanField(default=False)
    no_header = models.BooleanField(default=False)
    text = TranslateableField(null=True, blank=True,  max_length=80)
    help = TranslateableField(null=True, blank=True,  max_length=80)
    css_classes = models.CharField(max_length=50, null=True,default=None)

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


    def is_answered(self, session: Session):
        # TODO: Make this more variable if an answer could result in a text field value, for example.
        facette_widgets = apps.get_model("web", "FacetteSelectionWidget").objects.filter(
            pages__pk__in=[self.pk]
        )
        if facette_widgets.count() > 0:
            for widget in facette_widgets:
                has_selections = (
                    apps.get_model("web", "FacetteSelection").objects.filter(
                        session=session, facette__topic=widget.topic
                    ).count()
                    > 0
                )
                if has_selections:
                    return True
        return False
    
    def is_active(self, request: WebHttpRequest):
        return "page" in request.GET and request.GET.get("page") == self.catalogue_id
    
    @property
    def get_category(self) -> str:
        return apps.get_model("web", "Category").objects.get(target_page=self)

    @property
    def previous_page(self) -> Page | None:
        return Page.objects.filter(next_page=self).first()

    def next_visible_page(page: Page, session: Session) -> Page | None:
        # If the page is not visible, try to find a next displayable page.
        # TODO: Mind result in a null pointer
        fallback_page = None
        next_page = page.next_page

        next_page: Page
        while next_page is not None:
            if next_page.is_visible(session):
                fallback_page = next_page
                break
            next_page = next_page.next_page
        if fallback_page:
            page = fallback_page
        
        return page

    @property
    def widget_list(self) -> List[Widget]:
        # NavigationWidgets are the last set of widgets as they might need to know if errors appeared before.
        # TODO: Add hardware requirements widget (which requires some widgets to store abitrary data)


        # filter out the FacetteSelectionWidgets acting as parent for radio selections
        radio_selections = apps.get_model("web", "FacetteRadioSelectionWidget").objects.filter(pages__pk__in=[self])
        ignore_parent_selections = []
        for radio_selection in radio_selections:
            parent = radio_selection.__dict__["facetteselectionwidget_ptr_id"]
            ignore_parent_selections.append(parent)
        facette_selections = list( apps.get_model("web", "FacetteSelectionWidget").objects.exclude(pk__in=ignore_parent_selections).filter(pages__pk__in=[self]))
        return (
            list(SessionVersionWidget.objects.filter(pages__pk__in=[self]))
            + list(apps.get_model("web", "HTMLWidget").objects.filter(pages__pk__in=[self]))
            + list(radio_selections)
            + facette_selections
            + list(apps.get_model("web", "ResultListWidget").objects.filter(pages__pk__in=[self]))
            + list(apps.get_model("web", "ResultShareWidget").objects.filter(pages__pk__in=[self]))
            + list(apps.get_model("web", "NavigationWidget").objects.filter(pages__pk__in=[self]))
        )

    def proceed(self, request: WebHttpRequest) -> bool:
        for widget in self.widget_list:
            result = widget.proceed(request, self)
            if not result:
                return False

        return True

    @property
    def facette_selections(self) -> List:
        widgets_used = apps.get_model("web", "FacetteSelectionWidget").objects.filter(pages__pk__in=[self])
        return widgets_used

    @property
    def facette_selection_descriptions(self) -> List[str]:
        """
        Return a list of descriptions collected within FacetteSelectionWidgets of this page
        """
        result = list()
        widgets_used = self.facette_selections


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
        return PageMarking.objects.filter(page=self, session=session, is_error=False, is_warning=False).count() > 0
    def is_error(self, session: Session):
        return PageMarking.objects.filter(page=self, session=session, is_error=True).count() > 0
    def is_warning(self, session: Session):
        return PageMarking.objects.filter(page=self, session=session, is_warning=True).count() > 0

    def toggle_marking(self, session: Session):
        marking_matches = PageMarking.objects.filter(page=self, session=session, is_error=False, is_warning=False)

        if marking_matches.count() > 0:
            marking_matches.delete()
        else:
            marking = PageMarking(page=self, session=session)
            marking.save()

    def reset_answers(self, session: Session):
        widgets = self.widget_list
        for widget in widgets:
            if hasattr(widget, "topic"):
                topic = widget.topic
                facettes = Facette.objects.filter(topic=topic)
                for facette in facettes:
                    FacetteSelection.objects.filter(session=session,facette=facette).delete()

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
    is_error = models.BooleanField(default=False)
    is_warning = models.BooleanField(default=False)
    is_info = models.BooleanField(default=False)