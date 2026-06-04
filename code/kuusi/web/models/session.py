"""
distrochooser
Copyright (C) 2014-2026 Christoph Müller <distrochooser@chmr.eu>

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
from django.core.cache import cache

from kuusi.settings import RTL_LANGUAGES,PREVIOUS_VERSION_PREFIX

from sqids import Sqids
from time import time
from random import randint

from os import environ

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
    class EntryPointChoice(models.TextChoices):
        STARTPAGE = "STARTPAGE", "Start"
        ABOUT = "ABOUT", "About"
        CONTACT = "CONTACT", "Contact"
        PRIVACY = "PRIVACY", "Privacy"
        OUTGOING = "OUTGOING", "Outgoing link"
    entry_point = models.CharField(max_length=10,choices=EntryPointChoice.choices, default=None, null=True, blank=True)
    referrer = models.TextField(blank=True, default=None, null=True)
    # This is set at the time when a result is received
    # Crawler like sessions won't be acknowledged automatically
    is_ack = models.BooleanField(default=False)
    # A date time shall help to identify stay times for users
    ack_date_time =  models.DateTimeField(default=None, null=True, blank=True)
    
    language_code = models.CharField(max_length=10, default="en", null=False, blank=False)

    # to mark session imported from previous versions
    imported_from_session = models.CharField(max_length=10, default=None, null=True, blank=True)

    # See ADR 0028
    git_hash = models.CharField(max_length=50, default=None, null=True, blank=True)


    def get_meta_value(self, key: str) -> str | None:
        matches = SessionMeta.objects.filter(session=self, meta_key=key)
        if matches.count() < 1:
            return None
        match: SessionMeta = matches[0]
        return match.meta_value

    def __str__(self) -> str:
        return f"{self.result_id}"
    
    @property
    def is_rtl(self):
        return self.language_code in RTL_LANGUAGES

    
    @property
    def duration(self):
        if not self.is_ack or not self.ack_date_time:
            return "No duration"
        duration = self.ack_date_time - self.started 
        return str(duration)


    def get(result_id: str) -> Session:
        """
        Abstraction layer to allow access to Session objects

        Will use the Django cache as primar source, if not cached, return the live object. 

        If the live object is returned, it will be cached.
        """
        cache_key = f"session-{result_id}"
        cached = cache.get(cache_key)
        if cached:
            return cached
        non_cached = Session.objects.get(result_id=result_id)
        non_cached.cache()
        return non_cached
    
    def cache(self):
        """
        Put the object into Django's cache
        """
        cache_key = f"session-{self.result_id}"
        cache.delete(cache_key)
        cache.set(cache_key, self)
    
    def get_current_git_hash(self):
        if "GIT_HASH" in environ:
            return environ["GIT_HASH"]
        return None

    def save(self, **kwargs):
        git_hash = self.get_current_git_hash()
        if git_hash:
            self.git_hash = git_hash
        super().save(**kwargs)
        self.cache()

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
