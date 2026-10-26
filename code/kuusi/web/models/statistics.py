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
from user_agents import parse
from urllib3.util import parse_url
from calendar import monthrange
from datetime import timedelta


class TimeFrame(models.Model):
    name = models.CharField(blank=False, null=False)
    date = models.DateField(blank=True, null=True, default=None)
    end_date = models.DateField(blank=True, null=True, default=None)

    class TimeFrameType(models.TextChoices):
        MONTH = "MONTH", "MONTH"
        INTERVAL = "INTERVAL", "INTERVAL"

    time_frame_type = models.CharField(
        max_length=10,
        choices=TimeFrameType.choices,
        null=False,
        blank=False,
    )

    def __str__(self) -> str:
        return f"{self.time_frame_type}: {self.name}"

    @property
    def year(self) -> int:
        return self.date.year

    @property
    def result_count(self) -> int:
        return int(
            TimeFrameRow.objects.filter(
                time_frame=self,
                row_type=TimeFrameRow.TimeFrameRowType.ALL_COUNT,
                time_frame__time_frame_type=self.time_frame_type,
            )
            .first()
            .row_value_with_ack
        )

    @property
    def results(self) -> str:
        return f"{self.result_count} ({self.result_diff})"

    @property
    def hit_count(self) -> int:
        all_count = TimeFrameRow.objects.filter(
            time_frame=self,
            row_type=TimeFrameRow.TimeFrameRowType.ALL_COUNT,
            time_frame__time_frame_type=self.time_frame_type,
        ).first()
        return int(all_count.row_value_no_ack) + int(all_count.row_value_with_ack)

    @property
    def hit_diff(self) -> int:
        previous_entry = (
            TimeFrame.objects.order_by("date")
            .filter(
                date__lt=self.date,
                time_frame_type=self.time_frame_type,
            )
            .last()
        )
        if previous_entry:
            result = self.hit_count - previous_entry.hit_count
            return f"+{result}" if result > 0 else result
        else:
            return self.hit_count

    @property
    def hits(self) -> str:
        return f"{self.hit_count} ({self.hit_diff})"

    @property
    def daily_results(self) -> int:
        return round(
            self.result_count / monthrange(self.date.year, self.date.month)[1], 2
        )

    @property
    def daily_results_diff(self) -> str:
        previous_month = (
            TimeFrame.objects.order_by("date")
            .filter(
                date__lt=self.date,
                time_frame_type=self.time_frame_type,
            )
            .last()
        )
        if previous_month:
            result = round(self.daily_results - previous_month.daily_results, 2)
            return f"+{result}" if result > 0 else result
        else:
            return 0

    @property
    def daily(self) -> str:
        return f"{self.daily_results} ({self.daily_results_diff})"

    @property
    def result_diff(self) -> str:
        previous_month = (
            TimeFrame.objects.order_by("date")
            .filter(
                date__lt=self.date,
                time_frame_type=self.time_frame_type,
            )
            .last()
        )
        if previous_month:
            result = self.result_count - previous_month.result_count
            return f"+{result}" if result > 0 else result
        else:
            return 0

    @property
    def unique_backlinks(self) -> str:
        return TimeFrameRow.objects.filter(
            time_frame=self,
            row_type=TimeFrameRow.TimeFrameRowType.REFERRER,
            time_frame__time_frame_type=self.time_frame_type,
        ).count()

    @property
    def backlinks(self) -> str:
        previous_month = (
            TimeFrame.objects.order_by("date")
            .filter(
                date__lt=self.date,
                time_frame_type=self.time_frame_type,
            )
            .last()
        )
        if previous_month:
            result = self.unique_backlinks - previous_month.unique_backlinks
            diff = f"+{result}" if result > 0 else result
            return f"{self.unique_backlinks} ({diff})"
        return f"{self.unique_backlinks}"

    @property
    def top_result_domain(self) -> str:
        top_backlink = (
            TimeFrameRow.objects.filter(
                time_frame=self,
                row_type=TimeFrameRow.TimeFrameRowType.DOMAIN,
                time_frame__time_frame_type=self.time_frame_type,
            )
            .order_by("-row_value_with_ack")
            .first()
        )
        return f"{top_backlink.row_key} ({top_backlink.row_value_with_ack})"

    @property
    def top_hit_domain(self) -> str:
        top_backlink = (
            TimeFrameRow.objects.filter(
                time_frame=self,
                row_type=TimeFrameRow.TimeFrameRowType.DOMAIN,
                time_frame__time_frame_type=self.time_frame_type,
            )
            .order_by("-row_value_no_ack")
            .first()
        )
        return f"{top_backlink.row_key} ({top_backlink.row_value_no_ack})"

    @property
    def top_result_day(self) -> str:
        got = TimeFrameRow.objects.filter(
            time_frame=self,
            row_type=TimeFrameRow.TimeFrameRowType.TOP_DAY,
            time_frame__time_frame_type=self.time_frame_type,
        ).first()
        day_of_week = self.date.replace(day=int(got.row_key)).strftime("%a")
        if not got:
            return "?"
        diff = int(int(got.row_value_with_ack) - self.daily_results)
        return f"{day_of_week} {got.row_key}. {got.row_value_with_ack} ({"+" if diff > 0 else ""}{diff})"

    @property
    def worst_result_day(self) -> str:
        got = TimeFrameRow.objects.filter(
            time_frame=self,
            row_type=TimeFrameRow.TimeFrameRowType.WORST_DAY,
            time_frame__time_frame_type=self.time_frame_type,
        ).first()
        day_of_week = self.date.replace(day=int(got.row_key)).strftime("%a")
        if not got:
            return "?"
        diff = int(int(got.row_value_with_ack) - self.daily_results)
        return f"{day_of_week} {got.row_key}. {got.row_value_with_ack} ({"+" if diff > 0 else ""}{diff})"

    @property
    def top_result_os(self) -> str:
        got = (
            TimeFrameRow.objects.filter(
                time_frame=self,
                row_type=TimeFrameRow.TimeFrameRowType.OS,
                time_frame__time_frame_type=self.time_frame_type,
            )
            .order_by("-row_value_with_ack")
            .first()
        )

        return f"{got.row_key} ({got.row_value_with_ack})"

    @property
    def top_hit_os(self) -> str:
        got = (
            TimeFrameRow.objects.filter(
                time_frame=self,
                row_type=TimeFrameRow.TimeFrameRowType.OS,
                time_frame__time_frame_type=self.time_frame_type,
            )
            .order_by("-row_value_no_ack")
            .first()
        )

        return f"{got.row_key} ({got.row_value_no_ack})"

    @property
    def raw_duration(self) -> float:
        got = (
            TimeFrameRow.objects.filter(
                time_frame=self,
                row_type=TimeFrameRow.TimeFrameRowType.DURATION,
                time_frame__time_frame_type=self.time_frame_type,
            )
            .order_by("-row_value_with_ack")
            .first()
        )

        return float(got.row_value_with_ack)

    @property
    def duration(self) -> str:
        previous_month = (
            TimeFrame.objects.order_by("date")
            .filter(
                date__lt=self.date,
                time_frame_type=self.time_frame_type,
            )
            .last()
        )
        self_duration = timedelta(seconds=self.raw_duration)
        if previous_month:
            diff = int(self.raw_duration - previous_month.raw_duration)
            return f"{self_duration} ({"+" if diff > 0 else ""}{diff}s)"

        return f"{self_duration}"

    @property
    def container_visiblility_raw(self) -> int:
        got = (
            TimeFrameRow.objects.filter(
                time_frame=self,
                row_type=TimeFrameRow.TimeFrameRowType.CTR_TEST,
                time_frame__time_frame_type=self.time_frame_type,
            )
            .order_by("-row_value_with_ack")
            .first()
        )
        visibility_count = int(got.row_value_no_ack) + int(got.row_value_with_ack)
        all_count = self.hit_count + self.result_count
        if all_count == 0:
            return 0
        return round(visibility_count / all_count, 5)

    @property
    def container_visiblility(self) -> str:
        previous_month = (
            TimeFrame.objects.order_by("date")
            .filter(
                date__lt=self.date,
                time_frame_type=self.time_frame_type,
            )
            .last()
        )
        if previous_month:
            diff = float(
                self.container_visiblility_raw
                - previous_month.container_visiblility_raw
            )
            return (
                f"{self.container_visiblility_raw}% ({"+" if diff > 0 else ""}{diff}%)"
            )

        return f"{self.container_visiblility_raw}%"


class TimeFrameRow(models.Model):
    time_frame = models.ForeignKey(to=TimeFrame, null=False, on_delete=models.CASCADE)

    class TimeFrameRowType(models.TextChoices):
        LANGUAGE = "LANGUAGE", "LANGUAGE"
        ENTRY_POINT = "ENTRY_POINT", "ENTRY_POINT"
        ALL_COUNT = "ALL_COUNT", "ALL_COUNT"
        USER_AGENT = "USER_AGENT", "USER_AGENT"
        OS = "OS", "OS"
        OS_VERSION = "OS_VERSION", "OS_VERSION"
        BROWSER = "BROWSER", "BROWSER"
        CRAWLER = "CRAWLER", "CRAWLER"
        MOBILE = "MOBILE", "MOBILE"
        REFERRER = "REFERRER", "REFERRER"
        DOMAIN = "DOMAIN", "DOMAIN"
        TOP_DAY = "TOP_DAY", "TOP_DAY"
        WORST_DAY = "WORST_DAY", "WORST_DAY"
        DURATION = "DURATION", "DURATION"
        CTR_TEST = "CTR_TEST", "CTR_TEST"

        def transform(
            row_type: TimeFrameRowType.choices, value: str
        ) -> str | dict[str, str]:
            if value is None:
                value = "Unknown"
            if row_type == TimeFrameRow.TimeFrameRowType.USER_AGENT and value:
                ua = parse(value)
                values = {
                    TimeFrameRow.TimeFrameRowType.OS: ua.os.family,
                    TimeFrameRow.TimeFrameRowType.OS_VERSION: f"{ua.os.family} {ua.os.version_string}",
                    TimeFrameRow.TimeFrameRowType.BROWSER: ua.browser.family,
                }
                if ua.is_bot:
                    values[TimeFrameRow.TimeFrameRowType.CRAWLER] = value
                if ua.is_mobile:
                    values[TimeFrameRow.TimeFrameRowType.MOBILE] = ua.os.family
                return values
            elif row_type == TimeFrameRow.TimeFrameRowType.REFERRER and value:
                try:
                    parts = parse_url(value)
                    results = {
                        TimeFrameRow.TimeFrameRowType.REFERRER: value,
                        TimeFrameRow.TimeFrameRowType.DOMAIN: parts.netloc,
                    }

                    return results
                except Exception as e:
                    pass

            return {row_type: value}

    row_type = models.CharField(
        max_length=12,
        choices=TimeFrameRowType.choices,
        null=False,
        blank=False,
    )

    row_key = models.CharField(null=True, blank=True, default=None)
    row_value_with_ack = models.CharField(null=True, blank=True, default=None)
    row_value_no_ack = models.CharField(null=True, blank=True, default=None)
    ack_percentage = models.FloatField(default=0, blank=False)

    def save(self, **kwargs):
        ack_sums = self.row_value_no_ack + self.row_value_with_ack
        ack_percentage = 0
        if ack_sums > 0:
            ack_percentage = round(
                self.row_value_with_ack / ack_sums,
                2,
            )
        self.ack_percentage = ack_percentage
        super().save(**kwargs)

    def __str__(self) -> str:
        suffix = " " + self.row_key if self.row_key else ""
        return f"[{self.time_frame}] {self.row_type}{suffix}:  {self.row_value_with_ack} ({self.row_value_no_ack})"
