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

from django.core.management.base import BaseCommand, CommandParser
from web.models import Session, TimeFrame, TimeFrameRow
from termcolor import colored
from tqdm import tqdm
from django.utils.timezone import now
from django.utils.dateparse import parse_datetime
from datetime import timedelta


class Command(BaseCommand):
    help = "Generate statistics"

    def add_arguments(self, parser: CommandParser):
        parser.add_argument("--start_date", type=str, nargs="?")
        parser.add_argument("--end_date", type=str, nargs="?")
        parser.add_argument("--year", type=int, nargs="?")

    def handle(self, *args, **options):
        year = options["year"]
        timeframe_type = TimeFrame.TimeFrameType.MONTH
        end_date = None
        start_date = None
        start_option = options["start_date"]
        if year:
            start_date = parse_datetime(f"{year}-01-01 00:00:00").astimezone()
            end_date = parse_datetime(f"{year}-12-31 23:59:59").astimezone()
        else:

            end_date = (
                now()
                if not options["end_date"]
                else parse_datetime(options["end_date"])
            ).astimezone()
            if start_option:
                start_date = parse_datetime(start_option).astimezone()
                timeframe_type = TimeFrame.TimeFrameType.INTERVAL
            else:
                start_date = end_date.replace(
                    day=1, hour=0, minute=0, second=0, microsecond=0
                )
        if (end_date - start_date).days <= 1:
            raise Exception("Invalid dates")

        print(
            f"Timespan is {colored(start_date, 'magenta')} to {colored(end_date, 'red')}"
        )
        sessions = Session.objects.filter(
            started__gte=start_date, started__lte=end_date
        ).order_by("started")
        print(f"Found {colored(sessions.count(), "magenta")} session")

        timeframe_groups = {}

        for session in tqdm(sessions):
            month_str = session.started.strftime(
                "%Y-%m"
            )  # TODO: Derive from timeframe_type
            if month_str not in timeframe_groups:
                timeframe_groups[month_str] = []

            timeframe_groups[month_str].append(session)

        print(
            f"Found {colored(timeframe_groups.keys().__len__(), "magenta")} groups for time frame type {colored(timeframe_type, 'yellow')}"
        )

        key_str: str
        sessions: list[Session]
        for key_str, sessions in timeframe_groups.items():
            start_date = parse_datetime(f"{key_str}-01 00:00:00").astimezone()
            is_existing = (
                TimeFrame.objects.filter(
                    name=key_str, date=start_date, time_frame_type=timeframe_type
                ).count()
                > 0
            )

            if not is_existing:
                frame = TimeFrame(
                    name=key_str, time_frame_type=timeframe_type, date=start_date
                )
                frame.save()

            frame = TimeFrame.objects.get(
                name=key_str, time_frame_type=timeframe_type, date=start_date
            )

            ## Generic informations

            all_count = len(sessions)
            all_with_ack_count = len(list(filter(lambda s: s.is_ack, sessions)))

            container_visible_with_ack = len(
                list(filter(lambda s: s.is_ack and s.is_container_visible, sessions))
            )
            container_visible_no_ack = len(
                list(
                    filter(lambda s: not s.is_ack and s.is_container_visible, sessions)
                )
            )

            language_codes = {}
            entry_points = {}

            prop_map = {}
            properties = ["language_code", "entry_point", "user_agent", "referrer"]
            row_types = {
                "language_code": TimeFrameRow.TimeFrameRowType.LANGUAGE,
                "entry_point": TimeFrameRow.TimeFrameRowType.ENTRY_POINT,
                "user_agent": TimeFrameRow.TimeFrameRowType.USER_AGENT,
                "referrer": TimeFrameRow.TimeFrameRowType.REFERRER,
            }

            day_results = {}
            duration_sum = 0
            for s in tqdm(sessions):
                day = s.started.strftime("%d")
                if day not in day_results:
                    day_results[day] = 0
                day_results[day] += 1
                if s.is_ack and s.ack_date_time:
                    duration_sum += (s.ack_date_time - s.started).seconds
                for prop in properties:
                    row_type = row_types[prop]

                    attribute_value = s.__getattribute__(prop)
                    transformed_value = TimeFrameRow.TimeFrameRowType.transform(
                        row_type, attribute_value
                    )
                    for item_type, prop_value in transformed_value.items():
                        if item_type not in prop_map:
                            prop_map[item_type] = {}
                        if prop_value not in prop_map[item_type]:
                            prop_map[item_type][prop_value] = [0, 0]

                        with_ack_count = prop_map[item_type][prop_value][0] + (
                            1 if s.is_ack else 0
                        )
                        no_ack_count = prop_map[item_type][prop_value][1] + (
                            1 if not s.is_ack else 0
                        )
                        prop_map[item_type][prop_value] = [
                            with_ack_count,
                            no_ack_count,
                        ]
            TimeFrameRow.objects.filter(time_frame=frame).delete()
            for prop_type, stats in prop_map.items():
                for key, value in stats.items():
                    row_value_with_ack = value[0]
                    row_value_no_ack = value[1]

                    TimeFrameRow(
                        time_frame=frame,
                        row_type=prop_type,
                        row_key=key,
                        row_value_with_ack=row_value_with_ack,
                        row_value_no_ack=row_value_no_ack,
                    ).save()

            TimeFrameRow(
                time_frame=frame,
                row_type=TimeFrameRow.TimeFrameRowType.ALL_COUNT,
                row_value_with_ack=all_with_ack_count,
                row_value_no_ack=all_count - all_with_ack_count,
            ).save()
            top_day_key = None
            top_day_sessions = 0
            worst_day_key = None
            worst_day_sessions = 9999999999999999999999
            for day, session_count in day_results.items():
                if session_count > top_day_sessions:
                    top_day_key = day
                    top_day_sessions = session_count
                if session_count < worst_day_sessions:
                    worst_day_sessions = session_count
                    worst_day_key = day

            TimeFrameRow(
                time_frame=frame,
                row_type=TimeFrameRow.TimeFrameRowType.TOP_DAY,
                row_key=top_day_key,
                row_value_with_ack=top_day_sessions,
                row_value_no_ack=0,
            ).save()

            TimeFrameRow(
                time_frame=frame,
                row_type=TimeFrameRow.TimeFrameRowType.WORST_DAY,
                row_key=worst_day_key,
                row_value_with_ack=worst_day_sessions,
                row_value_no_ack=0,
            ).save()

            average_duration = 0
            if all_with_ack_count > 0:
                average_duration = duration_sum / all_with_ack_count
            TimeFrameRow(
                time_frame=frame,
                row_type=TimeFrameRow.TimeFrameRowType.DURATION,
                row_key=None,
                row_value_with_ack=average_duration,
                row_value_no_ack=0,
            ).save()

            TimeFrameRow(
                time_frame=frame,
                row_type=TimeFrameRow.TimeFrameRowType.CTR_TEST,
                row_key=None,
                row_value_with_ack=container_visible_with_ack,
                row_value_no_ack=container_visible_no_ack,
            ).save()
