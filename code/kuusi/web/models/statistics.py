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


class TimeFrame(models.Model):
    name = models.CharField(blank=False, null=False)
    date = models.DateField(blank=True, null=True, default=None)

    class TimeFrameType(models.TextChoices):
        MONTH = "MONTH", "MONTH"

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
                time_frame=self, row_type=TimeFrameRow.TimeFrameRowType.ALL_COUNT
            )
            .first()
            .row_value_with_ack
        )

    @property
    def daily_results(self) -> int:
        return round(
            self.result_count / monthrange(self.date.year, self.date.month)[1], 2
        )

    @property
    def diff(self) -> str:
        previous_month = (
            TimeFrame.objects.order_by("date").filter(date__lt=self.date).last()
        )
        if previous_month:
            result = self.result_count - previous_month.result_count
            return f"+{result}" if result > 0 else result
        else:
            return 0

    @property
    def active_domains(self) -> str:
        return TimeFrameRow.objects.filter(
            time_frame=self, row_type=TimeFrameRow.TimeFrameRowType.DOMAIN
        ).count()

    @property
    def top_domain(self) -> str:
        top_backlink = (
            TimeFrameRow.objects.filter(
                time_frame=self, row_type=TimeFrameRow.TimeFrameRowType.DOMAIN
            )
            .order_by("-row_value_with_ack")
            .first()
        )
        return f"{top_backlink.row_key} ({top_backlink.row_value_with_ack})"

    @property
    def top_result_day(self) -> str:
        got = TimeFrameRow.objects.filter(
            time_frame=self, row_type=TimeFrameRow.TimeFrameRowType.TOP_DAY
        ).first()
        day_of_week = self.date.replace(day=int(got.row_key)).strftime("%a")
        if not got:
            return "?"
        diff = int(int(got.row_value_with_ack) - self.daily_results)
        return f"{got.row_key}. ({day_of_week}, {got.row_value_with_ack}, ({"+" if diff > 0 else ""}{diff})"


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
        ack_percentage = round(
            self.row_value_with_ack / (self.row_value_no_ack + self.row_value_with_ack),
            2,
        )
        self.ack_percentage = ack_percentage
        super().save(**kwargs)

    def __str__(self) -> str:
        suffix = " " + self.row_key if self.row_key else ""
        return f"[{self.time_frame}] {self.row_type}{suffix}:  {self.row_value_with_ack} ({self.row_value_no_ack})"
