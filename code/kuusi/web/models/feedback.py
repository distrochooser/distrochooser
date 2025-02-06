"""
distrochooser
Copyright (C) 2014-2025  Christoph Müller  <mail@chmr.eu>

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

from .choosable import Choosable
from .facette import FacetteAssignment
from .session import Session


class Feedback(models.Model):
    choosable = models.ForeignKey(to=Choosable, null=False, on_delete=models.CASCADE)
    assignment = models.ForeignKey(
        to=FacetteAssignment, null=False, on_delete=models.CASCADE
    )
    is_positive = models.BooleanField(default=False)

    session = models.ForeignKey(
        to=Session,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="feedback_session",
    )

class LanguageFeedback(models.Model):
    session = models.ForeignKey(
        to=Session,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="language_feedback_session",
    )
    language_key = models.CharField(max_length=255, null=False)
    value = models.TextField(null=False)
    is_approved = models.BooleanField(default=False)


class LanguageFeedbackVote(models.Model):
    language_feedback = models.ForeignKey(
        to=LanguageFeedback,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="vote_language_feedback",
    )
    is_positive = models.BooleanField(default=False)