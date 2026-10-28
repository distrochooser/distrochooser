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

from django.db import models
from typing import List, Tuple, Dict
from os.path import exists
from web.models import Session, FacetteSelection, Facette, GivenFeedback
from web.management.commands.languagefeedback import Command as LanguageCommand
from django.core.management.base import BaseCommand, CommandParser
from logging import getLogger
from os.path import join, dirname, basename
from os import listdir
from kuusi.settings import AVAILABLE_LANGUAGES, DEFAULT_LANGUAGE_CODE
from termcolor import colored
from json import loads, dumps
from tqdm import tqdm
from dateutil.parser import parse
from datetime import datetime
import ijson
from django.utils import timezone

logger = getLogger("command")
ANSWER_MAP = {
    67: "live-mode-usage",
    66: "impaired-view-usage",
    65: "privacy-isolation-usage",
    35: "gaming-usage",
    34: "privacy-usage",
    33: "daily-usage",
    38: "professional-usage",
    37: "advanced-usage",
    36: "beginner-usage",
    41: "knowledge-present",
    40: "already-used",
    39: "no-linux-contact",
    44: "many-choices-gui",
    43: "scope-own-selection",
    42: "many-preselections",
    # 46+47 not mapped, as question is gone (old hardware question)
    48: "need-human-help",
    47: "manuals",
    50: "ux-concept-answer-mac-like",
    49: "ux-concept-answer-windows-like",
    53: "paid-support-ok",
    52: "pricing-free",
    55: "scope-own-selection",
    54: "scope-out-of-the-box",
    56: "license-open-source",
    57: "proprietary-okay-when-working",
    59: "okay-when-working",
    58: "privacy-no-connections-unless-wanted",
    64: "no-systemd",
    61: "software-admin-answer-console",
    60: "app-store-gui",
    63: "prefer-stable",
    62: "prefer-fast",
}

CHUNK_SIZE = 100000
WIPE_CHUNK_SIZE = 100000


class Command(BaseCommand):
    help = "Import a given set of Sessions from v5 into the database"

    def add_arguments(self, parser: CommandParser):
        parser.add_argument("user_session_path", type=str)
        parser.add_argument("given_answer_path", type=str)
        parser.add_argument("--wipe", action="store_true", default=False)
        parser.add_argument("--sessions", action="store_true", default=False)
        parser.add_argument("--feedbacks", action="store_true", default=False)
        parser.add_argument("--answers", action="store_true", default=False)

    def handle(self, *args, **options):
        print(
            f'Distrochooser {colored("v5", "light_cyan")} to {colored("v6", "green")} import'
        )
        given_answer_path = options["given_answer_path"]

        user_session_path = options["user_session_path"]

        if options["wipe"]:
            query = Session.objects.filter(
                imported_from_session__isnull=False
            )  # Will delete assignments and givenfeedback aswell
            while query.count():
                ids = query.values_list("pk", flat=True)[:WIPE_CHUNK_SIZE]
                got, _ = Session.objects.filter(pk__in=ids).delete()
                print(f'Deleted {colored(got, "red")} rows')

                query = Session.objects.filter(imported_from_session__isnull=False)

        if options["sessions"]:
            self.import_sessions(user_session_path)

        if options["answers"]:
            self.import_answers(given_answer_path)
        if options["feedbacks"]:
            self.import_feedback(user_session_path)

    def _is_language_present(self, needle: str) -> bool:
        for key, value in AVAILABLE_LANGUAGES:
            if key == needle:
                return True
        return False

    def get_answer_map(self) -> Dict[int, int]:
        answer_map = {}
        for key, value in ANSWER_MAP.items():
            answer_map[key] = Facette.objects.get(catalogue_id=value).pk
            print(
                f"Mapped facette {colored(key, 'yellow')} to {colored(value, 'green')}"
            )
        return answer_map

    def get_session_map(self) -> Dict[int, str]:
        session_map = {}
        all_sessions = Session.objects.filter(
            imported_from_session__isnull=False
        ).values("pk", "imported_from_session")
        print(
            f"{colored(all_sessions.count(), 'yellow')} sessions will be considered for mapping"
        )
        for session_tuple in tqdm(all_sessions):
            session_map[int(session_tuple["imported_from_session"])] = session_tuple[
                "pk"
            ]

        print(f"Mapping of old and new sessions {colored('done', 'green')} ")
        return session_map

    def import_feedback(self, path: str):
        total = 0
        now = timezone.now()
        with open(path, "r") as f:
            total = f.read().count("model")
        with open(path, "rb") as f:
            for session in tqdm(
                ijson.items(f, "item", use_float=True), unit=" sessions", total=total
            ):

                remark_text = session["fields"]["remarks"]
                session_id = session["pk"]
                if remark_text:
                    session_id = Session.objects.get(
                        imported_from_session=str(session_id)
                    ).pk
                    GivenFeedback.objects.filter(session_id=session_id).delete()
                    obj = GivenFeedback(
                        session_id=session_id,
                        text=f"{remark_text}",
                        import_date_time=now,
                    )
                    obj.save()

    def import_answers(self, path: str):
        # Map the ANSWER_MAP to _actual_ objects in the database
        # to avoid having to query per given answer over and over
        runtime_answer_map = self.get_answer_map()

        session_map = self.get_session_map()

        total = 0
        with open(path, "r") as f:
            total = f.read().count("model")
        selections = []
        now = timezone.now()
        with open(path, "rb") as f:
            for answer in tqdm(
                ijson.items(f, "item", use_float=True), unit=" answers", total=total
            ):
                if (
                    int(answer["fields"]["session"]) in session_map
                    and answer["fields"]["answer"] in runtime_answer_map
                ):
                    selections.append(
                        FacetteSelection(
                            facette_id=runtime_answer_map[answer["fields"]["answer"]],
                            session_id=session_map[
                                int(answer["fields"]["session"])
                            ],  # will be added on bulk
                            weight=2 if answer["fields"]["isImportant"] else 0,
                            imported_from_answer=answer["pk"],
                            import_date_time=now,
                        )
                    )
                if len(selections) == CHUNK_SIZE:
                    FacetteSelection.objects.bulk_create(
                        selections, ignore_conflicts=True
                    )
                    selections = []

    def import_sessions(self, path: str):

        new_sessions = []  # new session objects meant to bre created
        remarks = {}  # remarks to be created
        session_map = {}
        total = 0

        with open(path, "r") as f:
            total = f.read().count("model")

        now = timezone.now()
        with open(path, "rb") as f:
            for session_obj in tqdm(
                ijson.items(f, "item", use_float=True), unit=" sessions", total=total
            ):
                # Collect session properties which will be carried over
                session_id = session_obj["pk"]
                date_time = session_obj["fields"]["dateTime"]
                user_agent = session_obj["fields"]["userAgent"]
                result_id = session_obj["fields"]["publicUrl"]

                language = session_obj["fields"]["language"]
                if not self._is_language_present(language):
                    language = DEFAULT_LANGUAGE_CODE
                referrer = session_obj["fields"]["referrer"]
                is_ack = session_obj["fields"]["calculationEndTime"] is not None
                remark_text = session_obj["fields"]["remarks"]

                # Create the bulk creation objects for the new sessions
                new_session = Session(
                    started=date_time,
                    user_agent=user_agent,
                    result_id=result_id,
                    referrer=referrer,
                    is_ack=is_ack,
                    language_code=language,
                    imported_from_session=session_id,
                    ack_date_time=(
                        parse(session_obj["fields"]["calculationEndTime"])
                        if is_ack
                        else None
                    ),
                    import_date_time=now,
                )
                # As the sessions are created in bulk
                # The texts and the old ids will be collected
                # And created later on
                if remark_text is not None:
                    remarks[session_id] = remark_text

                new_sessions.append(new_session)

                if new_sessions.__len__() == CHUNK_SIZE:
                    # https://docs.djangoproject.com/en/6.1/ref/models/querysets/#django.db.models.query.QuerySet.bulk_create
                    created = Session.objects.bulk_create(
                        new_sessions, ignore_conflicts=True
                    )
                    for obj in created:
                        session_map[int(obj.imported_from_session)] = obj.pk
                    new_sessions = []
