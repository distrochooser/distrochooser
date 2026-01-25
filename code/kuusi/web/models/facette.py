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

from __future__ import annotations
from typing import List, Dict


from web.models import Translateable, TranslateableField, Session, Choosable
from django.db import models
from django.db.models import  QuerySet
from django.core.validators import MaxValueValidator, MinValueValidator
from django.apps import apps
from django.core.cache import cache
from kuusi.settings import LONG_CACHE_TIMEOUT, ENABLE_FEEDBACK_MODE

class Facette(Translateable):
    """
    A facette describes a fact narrowing down the selection for choosables.

    The description is displayed for selection within a page

    The topic reduces a facette to a certain subarea, e. g. "licenses" for Linux distributions
    """ 
    description = TranslateableField(null=False, blank=False, max_length=120)
    topic = models.CharField(null=False, blank=False, max_length=120)
    child_facettes = models.ManyToManyField(to="Facette", blank=True)

    @property
    def is_child(self) -> bool:
        return Facette.objects.filter(child_facettes__pk__in=[self.pk]).count() > 0

    @property
    def has_child(self) -> bool:
        return self.child_facettes.count() > 0
    
    @property
    def assignments(self) -> QuerySet[FacetteAssignment]:
        cache_key = f"facette-{self.pk}-assignments"
        cached = cache.get(cache_key)
        if cached:
            return cached
        assignments = FacetteAssignment.objects.filter(
            facettes__in=[self]
        )
        cache.set(cache_key, assignments)
        return assignments

    def __str__(self) -> str:
        msg_id = self.get_msgd_id_of_field("description")
        return f"[{self.topic}] (is_child: {self.is_child}, has_child: {self.has_child}) (msgid: {msg_id})"


class FacetteBehaviour(Translateable):
    affected_objects = models.ManyToManyField(
        to="Facette", blank=True, related_name="facette_behaviour_objects"
    )
    affected_subjects = models.ManyToManyField(
        to="Facette", blank=True, related_name="facette_behaviour_subjects"
    )

    def facette_in_queryset(self, selections: QuerySet[FacetteSelection], queryset: QuerySet):
        for selection in selections:
            facette = selection.facette
            if queryset.filter(pk=facette.pk).count() > 0:
                return True
        return False

    def is_true(self, facette: Facette, all_selections: QuerySet[FacetteSelection]) -> bool:
        is_subject = self.affected_subjects.filter(pk=facette.pk).count() > 0
        is_object = self.affected_objects.filter(pk=facette.pk).count() > 0
        is_subjects_others = self.facette_in_queryset(all_selections.exclude(facette=facette), self.affected_subjects)
        is_objects_others = self.facette_in_queryset(all_selections.exclude(facette=facette), self.affected_objects)

        if (is_subject or is_object) and (is_subjects_others or is_objects_others):
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
    # TODO: The facette is actually never an n=2 set...
    facettes = models.ManyToManyField(to=Facette)
    description = TranslateableField(
        null=True, blank=True, default=None, max_length=800
    )
    is_approved = models.BooleanField(default=False)

    # The sources is just a comma separated list of links
    # to keep this simple & stupid, no new entity will be introduced.
    sources = models.CharField(null=True,blank=True,default=None, max_length=5000)

    def __str__(self) -> str:
        if self.pk is None:
            return f"Virtual: ({self.assignment_type})" 
        choosables_str = [c.name for c in self.choosables.all()]
        facettes_str = [f.catalogue_id for f in self.facettes.all()]
        return f"{choosables_str} -> {facettes_str} ({self.assignment_type})"

    def is_flagged(self, choosable: Choosable) -> bool:
        return apps.get_model("web", "Feedback").objects.filter(assignment=self, choosable=choosable).count() != 0

    def get_votes(self) -> List[List[int, int, int]]:
        # do not search for anythin if the feedback mode is inactive
        if not ENABLE_FEEDBACK_MODE:
            return []
        # TODO: This is good for a MVP, but array nesting is utterly ugly. Wrap somewhere into the choosables at some point
        # If the Assignment is virtual (no pk) -> there are no votes
        if self.pk is None:
            return []
        cache_key = f"facetteassignment-{self.pk}-votes"
        cached = cache.get(cache_key)
        if cached is not None:
            return cached
        choosables = Choosable.objects.all()
        result = []
        votes = apps.get_model("web", "Feedback").objects.filter(assignment=self)
        choosable: Choosable
        for choosable in choosables:
            votes_choosable =  votes.filter(choosable=choosable)
            item = [
                choosable.pk,
                votes_choosable.filter(is_positive=True).count(),
                votes_choosable.filter(is_positive=False).count(),
            ]
            if item[1] > 0 or item[2] > 0:
                result.append(item)
        cache.set(cache_key, result, LONG_CACHE_TIMEOUT)
        return result

    def __lt__(self, other):
        order = [
            FacetteAssignment.AssignmentType.POSITIVE,
            FacetteAssignment.AssignmentType.NEUTRAL,
            FacetteAssignment.AssignmentType.NEGATIVE,
            FacetteAssignment.AssignmentType.BLOCKING,
        ]
        my_index = order.index(self.assignment_type)
        other_index = order.index(other.assignment_type)
        return my_index > other_index
    
    class AssignmentType(models.TextChoices):
        POSITIVE = "POSITIVE", "POSITIVE"
        NEGATIVE = "NEGATIVE", "NEGATIVE"
        NEUTRAL = "NEUTRAL", "NEUTRAL"
        BLOCKING = "BLOCKING", "BLOCKING"
        
        @staticmethod
        def get_score_map():
            score_map = {}
            for key in FacetteAssignment.AssignmentType.choices:
                identifier, _ = key
                score_map[identifier] = 0
            score_map["SCORE"] = 0
            return score_map
    assignment_type = models.CharField(
        max_length=20, choices=AssignmentType.choices, default=AssignmentType.NEUTRAL
    )
