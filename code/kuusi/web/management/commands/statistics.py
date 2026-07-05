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
import user_agents
import statistics

class Command(BaseCommand):
    help = "test"

    def add_arguments(self, parser):
        parser.add_argument("user_session_path",  type=str)

    def handle(self, *args, **options):
        user_session_path = options["user_session_path"]

        sessions = loads(open(user_session_path, "r").read())
        sessions.sort(key=lambda s: s["pk"], reverse=False)

        stats = {}

        for session in tqdm(sessions):
            date_time = parse(session["fields"]["dateTime"])

            # count everything as it was on the 1st of the month
            date = date_time.replace(hour=0,minute=0,second=0,day=1)
            ua = user_agents.parse(session["fields"]["userAgent"])
            is_ack = session["fields"]["calculationEndTime"] is not None
            # use unix timestamp for easier sorting
            key =  date.strftime("%s")
            if key not in stats:
                stats[key] = {
                    "ack": 0,
                    "non_ack": 0,
                    "bot_ack": 0,
                    "bot_non_ack": 0,
                    "ack_stay_duration": [],
                    "ack_user_agents": [],
                    "ack_referrer": 0
                }
            # For acknowledged session: Calculate stay time from start to calculate time
            if is_ack:
                end_time = parse(session["fields"]["calculationEndTime"])
                stay_duration =  end_time -  date_time
                stats[key]["ack_stay_duration"].append(stay_duration.total_seconds())
        
            prefix = ""
            if ua.is_bot:
                prefix = "bot_"
            if is_ack:
                stats[key][f"{prefix}ack"] += 1
                if session["fields"]["userAgent"] not in stats[key]["ack_user_agents"]:
                    stats[key]["ack_user_agents"].append(session["fields"]["userAgent"])
                referrer =  session["fields"]["referrer"] 
                if referrer and "distrochooser.de" not in referrer:
                    stats[key]["ack_referrer"] += 1
            else:
                stats[key][f"{prefix}non_ack"] += 1
            

            
        stats = dict(sorted(stats.items()))
        with open("stats.csv", "w") as file:
            file.write("day;ack;non_ack;bot_ack;bot_non_ack;ack_stay_duration;ack_user_agents;ack_referrer\n")
            for key, value in stats.items():
                ack = value["ack"]
                non_ack = value["non_ack"]
                bot_ack = value["bot_ack"]
                bot_non_ack = value["bot_non_ack"]
                ack_stay_duration = 0
                ack_user_agents = len(value["ack_user_agents"])
                ack_referrer = value["ack_referrer"]
                if len(value["ack_stay_duration"]) > 0:
                    ack_stay_duration = sum(value["ack_stay_duration"])/len(value["ack_stay_duration"])
                file.write(f"{key};{ack};{non_ack};{bot_ack};{bot_non_ack};{ack_stay_duration};{ack_user_agents};{ack_referrer}\n")

        