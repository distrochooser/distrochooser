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
        parser.add_argument("start_date", type=str) # Use UTC here
        parser.add_argument("--chunk", action="store_true", default=False)

    def handle(self, *args, **options):
        print(f'Distrochooser {colored("v5", "light_cyan")} to {colored("v6", "green")} import')
        user_session_path = options["user_session_path"]
        given_answer_path = options["given_answer_path"]
        start_date_raw = options["start_date"]
        start_date = parse(start_date_raw)
        if options["chunk"]:
            self._chunk_answers(user_session_path, given_answer_path)
            return

        self.import_sessions(user_session_path, given_answer_path, start_date)

    def _is_language_present(self, needle: str) -> bool:
        for key, value in AVAILABLE_LANGUAGES:
            if key == needle: 
                return True
        return False

    def _chunk_answers(self, path: str, given_answers_path: str):
        given_answers = []
        sessions = []
        given_answers_count = 0
        session_count = 0
        with open(given_answers_path, "r") as file:
            given_answers = loads(file.read())
            given_answers_count = len(given_answers)
            print(f"Found {colored(given_answers_count, 'yellow')} given answers.")
        
        given_answers.sort(key=lambda a: a["fields"]["session"] , reverse=False)
        chunks = self._chunks(given_answers, CHUNK_SIZE)
        index = 0
        for chunk in chunks:
            start = (index)*CHUNK_SIZE
            end = (index+1)*CHUNK_SIZE
            suffix = f"{start}-{end}"
            index +=1
            path = join(given_answers_path + "." + suffix)
            with open(path, "w") as file:
                file.write(dumps(chunk))

    def _chunks(self, lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]


    def import_sessions(self, path: str, given_answer_path: str, start_date: datetime):
        # clean up imported sessiont o prevent redundancies
        given_answers = []

        # Map the ANSWER_MAP to _actual_ objects in the database 
        # to avoid having to query per given answer over and over
        runtime_answer_map = {}
        for key, value in ANSWER_MAP.items():
            runtime_answer_map[key] = Facette.objects.get(catalogue_id=value)
            print(f"Mapped facette {colored(key, 'yellow')} to {colored(value, 'green')}")


        # The answer files are split into chunks (by their session's pk)
        # So the _actual_ answers must be mapped by the sessions' pk
        # The chunks will not be used until a set of sessions requires their usage
        answer_basename = basename(given_answer_path)
        answer_dirname = dirname(given_answer_path)
        answer_files = list(filter(lambda f: answer_basename in f and f != answer_basename, listdir(answer_dirname)))
        answer_files.sort()

        for file in answer_files:
            full_path = join(answer_dirname, file)
            parts = file.split(".")
            offset = parts[3].split("-")
            start = int(offset[0])
            end = int(offset[1])
            data = loads(open(full_path, "r").read())
            given_answers.append({
                "start": start,
                "end": end,
                "answers":data
            })

            given_answers_count = len(data)
        print(f"Processed {colored(len(answer_files), 'magenta')} given answer chunks")



        sessions =  []
        with open(path, "r") as file:
            sessions = loads(file.read())
            session_count = len(sessions)
            print(f"Found {colored(session_count, 'light_blue')} sessions.")
            sessions =  [s for s in sessions if parse(s["fields"]["dateTime"]) >= start_date]
            session_count = len(sessions)
            print(f"Found {colored(session_count, 'light_blue')} sessions after cutoff start date {colored(start_date, 'magenta')}")

            sessions.sort(key=lambda s: s["pk"], reverse=False)



        new_sessions = [] # new session objects meant to bre created
        old_session_ids = [] # session ids' of the session to be created
        known_sessions = {} # session objects created in the bulk, allowing to re-use objects to prevent multiple queriying. Will be cleared after the bulk
        remarks = {} # remarks to be created

        
        sessionion_obj: Dict
        for session_obj in tqdm(sessions):
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
                imported_from_session=session_id
            )

            # The session_ids which arte processed are collected to map the chunks for the given answers on create
            # the session ids are collected to easier match the answers when creating the bulk
            old_session_ids.append(session_id) 
            new_sessions.append(new_session)

            if new_sessions.__len__() == 1000:
                Session.objects.bulk_create(new_sessions)

                # find matching chunk for the given answers per bulk
                chunks_to_use = []
                for session_id in old_session_ids:
                    for chunk_index, chunk in enumerate(given_answers):
                        if chunk["start"] <= session_id and chunk["end"] >= session_id and chunk_index not in chunks_to_use:
                            chunks_to_use.append(chunk_index)


                # build the answer package
                raw_answers = []
                for chunk_index in chunks_to_use:
                    raw_answers += given_answers[chunk_index]["answers"]

                # extrac tthe answers matching the actual sessions
                answers = [a for a in raw_answers if a["fields"]["session"] in old_session_ids]
                # Store the given answers as selections 
                selections = []
                for answer in answers:
                    answer_id = answer["pk"]

                    session_id = answer["fields"]["session"]
                    answer_pk = answer["fields"]["answer"]
                    if answer_pk in runtime_answer_map:
                        new_session = None
                        if session_id in known_sessions:
                            new_session = known_sessions[session_id]
                        else:
                            new_session = Session.objects.filter(imported_from_session=session_id).first()
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
                            selections.append(selection)
                    
                FacetteSelection.objects.bulk_create(selections)

                # As we _assume_ the pk's are ordered properly
                # We will reset the remembered id's and data
                # as they are already processed
                known_sessions = {}
                new_sessions =  []
                old_session_ids = []
            
        # Store the remarks 
        # after the sessions are actually stored
        remarks_count = remarks.keys().__len__()
        print(f"Found {colored(remarks_count, 'cyan')} remarks")
        for old_id, remark_text in remarks.items():
            session = Session.objects.filter(imported_from_session=old_id).first()
            obj = GivenFeedback(
                session=session,
                text=f"Migrated from v5: {remark_text}"
            )
            obj.save()
