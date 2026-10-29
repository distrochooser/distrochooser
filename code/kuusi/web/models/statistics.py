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
from django.utils.html import mark_safe


class TimeFrame(models.Model):
    name = models.CharField(blank=False, null=False)
    date = models.DateField(blank=True, null=True, default=None)
    end_date = models.DateField(blank=True, null=True, default=None)

    class TimeFrameType(models.TextChoices):
        MONTH = "MONTH", "MONTH"
        INTERVAL = "INTERVAL", "INTERVAL"
        YEAR = "YEAR", "YEAR"

    time_frame_type = models.CharField(
        max_length=10,
        choices=TimeFrameType.choices,
        null=False,
        blank=False,
    )

    def __str__(self) -> str:
        return f"{self.time_frame_type}: {self.date}-{self.end_date}"

    @property
    def rank(self) -> str:
        all_frames = list(
            TimeFrame.objects.filter(time_frame_type=self.time_frame_type)
        )

        all_frames.sort(key=lambda f: f.all_visitors_raw, reverse=True)

        rank = all_frames.index(self) + 1
        color = "grey"
        if rank == 1:
            color = "gold"
        elif rank == 2:
            color = "silver"
        elif rank == 3:
            color = "#e18787"
        return mark_safe(
            f"<span style='font-weight: bold; color:{color}'>{rank}.</span>"
        )

    @property
    def all_visitors_raw(self) -> int:
        previous_entry = (
            TimeFrame.objects.order_by("date")
            .filter(
                date__lt=self.date,
                time_frame_type=self.time_frame_type,
            )
            .last()
        )
        all_count = self.hit_count + self.result_count
        return all_count

    @property
    def all_visitors(self) -> str:
        previous_entry = (
            TimeFrame.objects.order_by("date")
            .filter(
                date__lt=self.date,
                time_frame_type=self.time_frame_type,
            )
            .last()
        )
        all_count = self.hit_count + self.result_count
        if previous_entry:
            average_diff = self.result_count - self.average("all_visitors_raw")
            average_diff_year = self.all_visitors_raw - self.average(
                "all_visitors_raw", False
            )
            diff = self.all_visitors_raw - previous_entry.all_visitors_raw
            return mark_safe(
                f"{all_count} ({self._coloring(diff)})<br/>{self._coloring(average_diff, "⌀")}<br/>{self._coloring(average_diff_year, "y⌀")}"
            )
        return all_count

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
        average_diff = self.result_count - self.average("result_count")
        average_diff_year = self.result_count - self.average("result_count", False)
        return mark_safe(
            f"{self.result_count} ({self._coloring(self.result_diff)})<br>{self._coloring(average_diff, "⌀")}<br>{self._coloring(average_diff_year, "y⌀")}"
        )

    @property
    def hit_count(self) -> int:
        all_count = TimeFrameRow.objects.filter(
            time_frame=self,
            row_type=TimeFrameRow.TimeFrameRowType.ALL_COUNT,
            time_frame__time_frame_type=self.time_frame_type,
        ).first()
        return int(all_count.row_value_no_ack)

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
            return self._coloring(result)
        else:
            return self.hit_count

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
            average_diff = self.daily_results - self.average("daily_results")
            average_diff_year = self.daily_results - self.average(
                "daily_results", False
            )
            return mark_safe(
                f"{self._coloring(result)}<br/>{self._coloring(average_diff, "⌀")}<br/>{self._coloring(average_diff_year, "y⌀")}"
            )
        else:
            return mark_safe(self._coloring(0))

    def _top_n_raw(self, what: TimeFrameRow.TimeFrameRowType, with_ack: bool = False):

        results = TimeFrameRow.objects.filter(
            time_frame=self,
            row_type=what,
            time_frame__time_frame_type=self.time_frame_type,
        ).order_by("-row_value_no_ack" if not with_ack else "-row_value_with_ack")

        if results.__len__() == 0:
            return {}

        got = {}
        for result in results:
            got[result.row_key] = (
                result.row_value_no_ack if not with_ack else result.row_value_with_ack
            )
        return got

    def _top_n(
        self, what: TimeFrameRow.TimeFrameRowType, with_ack: bool = False, n=3
    ) -> str:

        results = self._top_n_raw(what, with_ack)

        previous_month = (
            TimeFrame.objects.order_by("date")
            .filter(
                date__lt=self.date,
                time_frame_type=self.time_frame_type,
            )
            .last()
        )
        prev_month_results = {}
        if previous_month:
            prev_month_results = previous_month._top_n_raw(what, with_ack)

        got = ""
        amount = 0
        for key, count in results.items():
            diff_str = ""
            if key in prev_month_results:
                diff_raw = count - prev_month_results[key]
                diff_str = f", {self._coloring(diff_raw)}"
            got += f"{key} ({count}{diff_str})</br>"
            if amount >= n:
                break
            amount += 1
        return mark_safe(got)

    def _coloring(self, value: float, prefix="pm") -> str:
        color = "#8585fd"
        if value != 0:
            color = "#ff7b7b" if value < 0 else "#28fd28"
        return f"<span style='color: {color}'>{prefix}{"+" if value >= 0 else ""}{round(value, 2)}</span>"

    @property
    def top_language_hits(self) -> str:

        return self._top_n(TimeFrameRow.TimeFrameRowType.LANGUAGE)

    def top_language_results(self) -> str:
        return self._top_n(TimeFrameRow.TimeFrameRowType.LANGUAGE, with_ack=True)

    @property
    def daily(self) -> str:
        return mark_safe(f"{self.daily_results} ({self.daily_results_diff})")

    @property
    def top_hit_browser(self) -> str:
        return self._top_n(TimeFrameRow.TimeFrameRowType.BROWSER)

    @property
    def top_result_browser(self) -> str:
        return self._top_n(TimeFrameRow.TimeFrameRowType.BROWSER, with_ack=True)

    @property
    def top_hit_crawlers(self) -> str:
        return self._top_n(TimeFrameRow.TimeFrameRowType.CRAWLER, n=3)

    @property
    def crawler_with_result(self) -> str:
        got = self._top_n_raw(
            TimeFrameRow.TimeFrameRowType.CRAWLER, with_ack=True
        ).values()
        summarized = 0
        for got in got:
            summarized += got
        return "yes" if summarized > 0 else "no"

    def average(self, property_name: str, overall=True) -> float:
        frames = (
            TimeFrame.objects.exclude(pk=self.pk, time_frame_type=self.time_frame_type)
            if overall
            else TimeFrame.objects.filter(date__year=self.date.year).exclude(
                pk=self.pk, time_frame_type=self.time_frame_type
            )
        )
        sum_value = 0
        for frame in frames:
            sum_value += float(frame.__getattribute__(property_name))

        return sum_value / frames.count() if frames.count() > 0 else 0

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
            return result
        else:
            return 0

    @property
    def unique_backlinks(self) -> int:
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
            average_diff = self.unique_backlinks - self.average("unique_backlinks")
            average_diff_year = self.unique_backlinks - self.average(
                "unique_backlinks", False
            )
            result = self.unique_backlinks - previous_month.unique_backlinks
            return mark_safe(
                f"{self.unique_backlinks} ({self._coloring(result)})<br/>{self._coloring(average_diff, "⌀")}<br/>{self._coloring(average_diff_year, "y⌀")}"
            )
        return f"{self.unique_backlinks}"

    @property
    def top_result_domain(self) -> str:
        return self._top_n(TimeFrameRow.TimeFrameRowType.DOMAIN, True)

    @property
    def top_hit_domain(self) -> str:
        return self._top_n(TimeFrameRow.TimeFrameRowType.DOMAIN, False)

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
        return mark_safe(
            f"{day_of_week} {got.row_key}. {got.row_value_with_ack} ({self._coloring(diff)})"
        )

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
        return mark_safe(
            f"{day_of_week} {got.row_key}. {got.row_value_with_ack} ({self._coloring(diff)})"
        )

    @property
    def top_result_os(self) -> str:
        return self._top_n(TimeFrameRow.TimeFrameRowType.OS, with_ack=True)

    @property
    def top_hit_os(self) -> str:
        return self._top_n(TimeFrameRow.TimeFrameRowType.OS)

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

            average_diff = self.raw_duration - self.average("raw_duration")
            average_diff_year = self.raw_duration - self.average("raw_duration", False)
            return mark_safe(
                f"{self_duration} ({self._coloring(diff)}s)<br/>{self._coloring(average_diff, "⌀")}<br/>{self._coloring(average_diff_year, "y⌀")}"
            )

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
        return round((visibility_count / all_count) * 100, 3)

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
            return mark_safe(
                f"{self.container_visiblility_raw}% ({self._coloring(diff)})"
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
        CRAWLER_UA = "CRAWLER_UA", "CRAWLER_UA"
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
                    values[TimeFrameRow.TimeFrameRowType.CRAWLER_UA] = value
                    values[TimeFrameRow.TimeFrameRowType.CRAWLER] = ua.browser.family
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
    row_value_with_ack = models.IntegerField(null=False, blank=False, default=0)
    row_value_no_ack = models.IntegerField(null=False, blank=False, default=0)
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
