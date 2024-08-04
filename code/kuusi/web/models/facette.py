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
from typing import List, Dict


from web.models import Translateable, TranslateableField, Session, Choosable
from django.db import models
from django.db.models import  QuerySet
from django.core.validators import MaxValueValidator, MinValueValidator
from django.apps import apps

class Facette(Translateable):
    """
    A facette describes a fact narrowing down the selection for choosables.

    The selectable_description is displayed for selection within a page

    The topic reduces a facette to a certain subarea, e. g. "licenses" for Linux distributions
    """ 

    # TODO: Add a source flag to describe decisions.

    selectable_description = TranslateableField(null=False, blank=False, max_length=120)
    topic = models.CharField(null=False, blank=False, max_length=120)
    child_facettes = models.ManyToManyField(to="Facette", blank=True)

    @property
    def is_child(self) -> bool:
        return Facette.objects.filter(child_facettes__pk__in=[self.pk]).count() > 0

    @property
    def has_child(self) -> bool:
        return self.child_facettes.count() > 0

    def __str__(self) -> str:
        return f"[{self.topic}] (is_child: {self.is_child}, has_child: {self.has_child}) (select: {self.selectable_description})"


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
        is_subject = self.affected_subjects.filter(pk=facette.pk).count() > 0
        is_object = self.affected_objects.filter(pk=facette.pk).count() > 0
        is_subjects_others = self.facette_in_queryset(others, self.affected_subjects)
        is_objects_others = self.facette_in_queryset(others, self.affected_objects)

        if self.direction == FacetteBehaviour.Direction.BIDIRECTIONAL:
            if (is_subject or is_object) and (is_subjects_others or is_objects_others):
                return True

        if self.direction == FacetteBehaviour.Direction.SUBJECT_TO_OBJECT:
            if is_subject and is_objects_others or is_subjects_others and is_object:
                return True

        if self.direction == FacetteBehaviour.Direction.OBJECT_TO_SUBJECT:
            if is_object and is_objects_others or is_subjects_others and is_object:
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
    long_description = TranslateableField(
        null=True, blank=True, default=None, max_length=800
    )

    def __str__(self) -> str:
        choosables_str = [c.name for c in self.choosables.all()]
        facettes_str = [f.catalogue_id for f in self.facettes.all()]
        return f"{choosables_str} -> {facettes_str} ({self.assignment_type})"

    def is_flagged(self, choosable: Choosable) -> bool:
        return apps.get_model("web", "Feedback").objects.filter(assignment=self, choosable=choosable).count() != 0


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
                FacetteAssignment.AssignmentType.BLOCKING: -100,
            }
            score = 0
            for key, value in haystack.items():
                score += score_map[key] * value
            
            return score

    assignment_type = models.CharField(
        max_length=20, choices=AssignmentType.choices, default=AssignmentType.NEUTRAL
    )
