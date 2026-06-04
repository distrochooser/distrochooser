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
from typing import List, Tuple, Dict
from os.path import exists
from web.models import Session, FacetteSelection, Facette, GivenFeedback
from web.management.commands.languagefeedback import Command as LanguageCommand
from django.core.management.base import BaseCommand 
from logging import getLogger
from os.path import join, dirname, basename
from os import listdir
from kuusi.settings import  AVAILABLE_LANGUAGES, DEFAULT_LANGUAGE_CODE
from termcolor import colored
from json import loads, dumps
from tqdm import tqdm
from dateutil.parser import parse
from datetime import datetime

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
    62: "prefer-fast"
}

CHUNK_SIZE = 100000
class Command(BaseCommand):
    help = "Import a given set of Sessions from v5 into the database"

    def add_arguments(self, parser):
        parser.add_argument("user_session_path",  type=str)
        parser.add_argument("given_answer_path", type=str)
        parser.add_argument("start_date", type=str) # Use UTC here, if an empty string is porvided, it is ignored

    def handle(self, *args, **options):
        print(f'Distrochooser {colored("v5", "light_cyan")} to {colored("v6", "green")} import')
        user_session_path = options["user_session_path"]
        given_answer_path = options["given_answer_path"]
        start_date_raw = options["start_date"]
        start_date = parse(start_date_raw) if start_date_raw else None
        self.import_sessions(user_session_path, given_answer_path, start_date)

    def _is_language_present(self, needle: str) -> bool:
        for key, value in AVAILABLE_LANGUAGES:
            if key == needle: 
                return True
        return False


    def import_sessions(self, path: str, given_answer_path: str, start_date: datetime | None):
        # clean up imported sessiont o prevent redundancies
        given_answers = []

        # Map the ANSWER_MAP to _actual_ objects in the database 
        # to avoid having to query per given answer over and over
        runtime_answer_map = {}
        for key, value in ANSWER_MAP.items():
            runtime_answer_map[key] = Facette.objects.get(catalogue_id=value)
            print(f"Mapped facette {colored(key, 'yellow')} to {colored(value, 'green')}")



        # Parse the raw answer and session files
        answers =  []
        with open(given_answer_path, "r") as file:
            answers = loads(file.read())
            answers_count = len(answers)
            print(f"Found {colored(answers_count, 'light_blue')} given answers.")

        sessions =  []
        with open(path, "r") as file:
            sessions = loads(file.read())
            session_count = len(sessions)
            print(f"Found {colored(session_count, 'light_blue')} sessions.")
            if start_date is not None:
                sessions =  [s for s in sessions if parse(s["fields"]["dateTime"]) >= start_date]
                session_count = len(sessions)
                print(f"Found {colored(session_count, 'light_blue')} sessions after cutoff start date {colored(start_date, 'magenta')}")
            else:
                print(f"{colored('Ignoring cutoff date.', 'red')}")
            sessions.sort(key=lambda s: s["pk"], reverse=False)


        # Step 1: Create sessions
        # Also collect remarks for later creation

        new_sessions = [] # new session objects meant to bre created
        remarks = {} # remarks to be created

        session_map = {}
        sessionion_obj: Dict
        for session_obj in tqdm(sessions):
            # Collect session properties which will be carried over
            session_id = str(session_obj["pk"])
            date_time = session_obj["fields"]["dateTime"]
            user_agent = session_obj["fields"]["userAgent"]
            result_id = session_obj["fields"]["publicUrl"]
            language = session_obj["fields"]["language"]
            if not self._is_language_present(language):
                language = DEFAULT_LANGUAGE_CODE
            referrer = session_obj["fields"]["referrer"]
            is_ack = session_obj["fields"]["calculationEndTime"] is not None
            remark_text = session_obj["fields"]["remarks"]

            # As the sessions are created in bulk
            # The texts and the old ids will be collected 
            # And created later on
            if remark_text is not None:
                remarks[session_id] = remark_text


            # Create the bulk creation objects for the new sessions
            new_session = Session(
                started=date_time,
                user_agent=user_agent,
                result_id=result_id,
                referrer=referrer,
                is_ack=is_ack,
                language_code=language,
                imported_from_session=session_id,
                ack_date_time=parse(session_obj["fields"]["calculationEndTime"]) if is_ack else None
            )

            new_sessions.append(new_session)

            if new_sessions.__len__() == 1000:
                created = Session.objects.bulk_create(new_sessions)
                for obj in created:
                    session_map[str(obj.imported_from_session)] = obj.pk
                new_sessions = []

        # Step 2: Create answers fro the given sessions

        print(f"Found {colored(len(answers), 'magenta')} given answers.")
        # Store the given answers as selections 
        selections = []
        for answer in tqdm(answers):
            answer_id = answer["pk"]

            session_id = str(answer["fields"]["session"])
            answer_pk = answer["fields"]["answer"]
            if answer_pk in runtime_answer_map:
                is_important = answer["fields"]["isImportant"]
                selection = FacetteSelection(
                    facette=runtime_answer_map[answer_pk],
                    session_id=session_map[session_id],
                    weight=2 if is_important else 0,
                    imported_from_answer=answer_id
                )  
                selections.append(selection)

            
            if len(selections) == 1000:
                FacetteSelection.objects.bulk_create(selections)
                selections = []


            
        # Store the remarks 
        # after the sessions are actually stored
        remarks_count = remarks.keys().__len__()
        print(f"Found {colored(remarks_count, 'cyan')} remarks")
        for old_id, remark_text in tqdm(remarks.items()):
            obj = GivenFeedback(
                session_id=session_map[old_id],
                text=f"Migrated from v5: {remark_text}"
            )
            obj.save()
