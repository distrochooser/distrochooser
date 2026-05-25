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
from web.models import Session, FacetteSelection, Facette
from web.management.commands.languagefeedback import Command as LanguageCommand
from django.core.management.base import BaseCommand 
from logging import getLogger
from os.path import join
from kuusi.settings import  AVAILABLE_LANGUAGES, DEFAULT_LANGUAGE_CODE
from termcolor import colored
from json import loads
from tqdm import tqdm
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

class Command(BaseCommand):
    help = "Import a given set of Sessions from v5 into the database"

    def add_arguments(self, parser):
        parser.add_argument("user_session_path",  type=str)
        parser.add_argument("given_answer_path", type=str)
        parser.add_argument("--delete", action="store_true", default=False)

    def handle(self, *args, **options):
        print(f'Distrochooser {colored("v5", "light_cyan")} to {colored("v6", "green")} import')
        user_session_path = options["user_session_path"]
        given_answer_path = options["given_answer_path"]

        if options["delete"]:
            print(f"{colored("Cleaning ob previous import results", 'yellow')}")
            old_sessions = Session.objects.filter(imported_from_session__isnull=False)
            for session in tqdm(old_sessions, unit="Session"):
                session.delete()
            old_answers = FacetteSelection.objects.filter(imported_from_answer__isnull=False)
            for selection in tqdm(old_answers, unit="Selections"):
                selection.delete()

        self.import_sessions(user_session_path, given_answer_path)

    def _is_language_present(self, needle: str) -> bool:
        for key, value in AVAILABLE_LANGUAGES:
            if key == needle: 
                return True
        return False
    
    def import_sessions(self, path: str, given_answer_path: str):
        # clean up imported sessiont o prevent redundancies
        given_answers = []

        runtime_answer_map = {}

        for key, value in ANSWER_MAP.items():
            runtime_answer_map[key] = Facette.objects.get(catalogue_id=value)

        with open(given_answer_path, "r") as file:
            given_answers = loads(file.read())
            given_answers_count = len(given_answers)
            print(f"Found {colored(given_answers_count, 'yellow')} given answers.")

        with open(path, "r") as file:
            content = loads(file.read())
            
            session_count = len(content)
            print(f"Found {colored(session_count, 'light_blue')} sessions.")

            stats = {
                "not_acknowledged": 0,
                "fallback_english": 0,
                "done": 0,
                "answers": 0
            }


            # FIXME: Add option to incrementally handle the import
            # FIXME: DB lock issue on local test instance
            new_sessions = []

            runtime_session_map = {}

            sessionion_obj: Dict
            for session_obj in tqdm(content, unit="session"):
                session_id = session_obj["pk"]
                date_time = session_obj["fields"]["dateTime"]
                user_agent = session_obj["fields"]["userAgent"]
                result_id = session_obj["fields"]["publicUrl"]
                language = session_obj["fields"]["language"]

                if not self._is_language_present(language):
                    language = DEFAULT_LANGUAGE_CODE
                    stats["fallback_english"] += 1

                remarks = session_obj["fields"]["remarks"]
                referrer = session_obj["fields"]["referrer"]
                is_ack = session_obj["fields"]["calculationEndTime"] is not None

                if not is_ack:
                    stats["not_acknowledged"] += 1

                new_session = Session(
                    started=date_time,
                    user_agent=user_agent,
                    result_id=result_id,
                    referrer=referrer,
                    is_ack=is_ack,
                    language_code=language,
                    imported_from_session=session_id
                )




                new_sessions.append(new_session)
                stats["done"] += 1

                if new_sessions.__len__() == 1000:
                    Session.objects.bulk_create(new_sessions)
                    new_sessions =  []
            

            # is these for bulk creation rather than one at a time
            new_selections  = []
            known_sessions = {}
        
            for answer in tqdm(given_answers,unit="answer"):
                answer_id = answer["pk"]

                session_id = answer["fields"]["session"]
                answer_pk = answer["fields"]["answer"]
                if answer_pk in runtime_answer_map:
                    # Only proceed if the answer is mapped within the runtime map
                    # which holds the facettes itself at import


                    # Reuse the known_session if possible to make this impoort more quick
                    new_session = None
                    if session_id in known_sessions:
                        new_session = known_sessions[session_id]
                    else:
                        new_session = Session.objects.get(imported_from_session=session_id)
                        known_sessions[session_id] = new_session


                    # only continue if ther eis a suitable session found
                    if new_session:
                        is_important = answer["fields"]["isImportant"]

                        selection = FacetteSelection(
                            facette=runtime_answer_map[answer_pk],
                            session=new_session,
                            weight=2 if is_important else 0,
                            imported_from_answer=answer_id
                        )  
                        new_selections.append(selection)

                        stats["answers"] += 1

                        if new_selections.__len__() == 1000:
                            FacetteSelection.objects.bulk_create(new_selections)
                            new_selections = []
                            known_sessions = {} # TO prevent exhaustion of RAM


            # TODO: Do somelthing propery with the stats
            print(stats)