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
from uuid import uuid4

from django.db import models
from django.utils import timezone

from kuusi.settings import RTL_LANGUAGES,PREVIOUS_VERSION_PREFIX

from sqids import Sqids
from time import time
from random import randint

def get_session_result_id() -> str:
    sqids = Sqids()
    seed = int(time())
    random_component = randint(0, 100000)
    id = sqids.encode([seed, random_component]) 
    # Add a prefix to the ID itself, to allow redirection
    return PREVIOUS_VERSION_PREFIX + id

class Session(models.Model):
    started = models.DateTimeField(default=timezone.now, null=False, blank=False)
    user_agent = models.CharField(default=None, null=True, blank=True, max_length=150)
    result_id = models.CharField(
        default=get_session_result_id, max_length=36, null=False, blank=False
    )
    version = models.ForeignKey(
        to="SessionVersion",
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        blank=True,
        related_name="session_version",
    )
    session_origin = models.ForeignKey(
        to="Session",
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        blank=True,
        related_name="session_sessionorigin",
    )
    referrer = models.TextField(blank=True, default=None, null=True)
    is_ack = models.BooleanField(default=False) # A session will be 'acknowledged' by a JS snippet to exclude curl() calls
    language_code = models.CharField(max_length=10, default="en", null=False, blank=False)

    def get_meta_value(self, key: str) -> str | None:
        matches = SessionMeta.objects.filter(session=self, meta_key=key)
        if matches.count() < 1:
            return None
        match: SessionMeta = matches[0]
        return match.meta_value

    def __str__(self) -> str:
        return f"{self.started}: {self.result_id}"
    
    @property
    def is_rtl(self):
        return self.language_code in RTL_LANGUAGES

class SessionMeta(models.Model):
    session = models.ForeignKey(
        to="Session",
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        blank=True,
        related_name="sessionmeta_session",
    )
    meta_key = models.CharField(max_length=30, null=False, blank=False)
    meta_value = models.CharField(max_length=30, null=False, blank=False)
    def __str__(self) -> str:
        return f"{self.session}: {self.meta_key} -> {self.meta_value}"
