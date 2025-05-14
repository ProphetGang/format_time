# time_engine/time.py

import logging

logger = logging.getLogger(__name__)


class Time:
    def __init__(
        self,
        ticks_per_hour: int = 1,
        hours_per_day: int = 24,
        days_per_month: int = 30,
        months_per_year: int = 12,
        lunar_cycle_days: int | None = None,
    ):
        # ✅ Defensive checks
        if ticks_per_hour <= 0:
            raise ValueError("ticks_per_hour must be positive")
        if hours_per_day <= 0:
            raise ValueError("hours_per_day must be positive")
        if days_per_month <= 0:
            raise ValueError("days_per_month must be positive")
        if months_per_year <= 0:
            raise ValueError("months_per_year must be positive")
        if lunar_cycle_days is not None and lunar_cycle_days <= 0:
            raise ValueError("lunar_cycle_days must be positive if specified")

        self.ticks_per_hour = ticks_per_hour
        self.hours_per_day = hours_per_day
        self._rollover_hours = hours_per_day

        self.days_per_month = days_per_month
        self.months_per_year = months_per_year

        self.lunar_cycle_days = (
            lunar_cycle_days
            if lunar_cycle_days is not None
            else self.days_per_month * self.months_per_year
        )
        self.days_per_year = self.days_per_month * self.months_per_year

        logger.debug(
            "Time.__init__: ticks_per_hour=%d, hours_per_day=%d, days_per_month=%d, "
            "months_per_year=%d, lunar_cycle_days=%d, days_per_year=%d",
            self.ticks_per_hour,
            self.hours_per_day,
            self.days_per_month,
            self.months_per_year,
            self.lunar_cycle_days,
            self.days_per_year,
        )

        self.tick = 0
        self.hour = 0
        self.day = 1
        self.month = 1
        self.year = 1

    def advance(self, ticks: int = 1) -> None:
        if not isinstance(ticks, int):
            raise TypeError("Ticks must be an integer")
        if ticks < 0:
            raise ValueError("Ticks must be non-negative")

        # 1) Ticks → Hours
        total_ticks = self.tick + ticks
        extra_hours, self.tick = divmod(total_ticks, self.ticks_per_hour)

        # 2) Hours → Days
        total_hours = self.hour + extra_hours
        extra_days, self.hour = divmod(total_hours, self.hours_per_day)

        # 3) Days → Months (zero-based adjustment)
        total_days_zero = (self.day - 1) + extra_days
        extra_months, day_zero = divmod(total_days_zero, self.days_per_month)
        self.day = day_zero + 1

        # 4) Months → Years (zero-based adjustment)
        total_months_zero = (self.month - 1) + extra_months
        extra_years, month_zero = divmod(total_months_zero, self.months_per_year)
        self.month = month_zero + 1

        # 5) Finally bump the year
        self.year += extra_years

        logger.debug(
            "Time.advance: +%d tick(s) → +%d hour(s), +%d day(s), +%d month(s), +%d year(s); "
            "now %d/%d/%d %d:%d",
            ticks,
            extra_hours,
            extra_days,
            extra_months,
            extra_years,
            self.year,
            self.month,
            self.day,
            self.hour,
            self.tick,
        )

    def current_datetime(self) -> dict:
        return {
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "hour": self.hour,
            "tick": self.tick,
        }

    def set_datetime(
        self, year: int, month: int, day: int, hour: int, tick: int
    ) -> None:
        if year < 1:
            raise ValueError("Invalid year")
        if not (1 <= month <= self.months_per_year):
            raise ValueError("Invalid month")
        if not (1 <= day <= self.days_per_month):
            raise ValueError("Invalid day")
        if not (0 <= hour < self.hours_per_day):
            raise ValueError("Invalid hour")
        if not (0 <= tick < self.ticks_per_hour):
            raise ValueError("Invalid tick")

        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.tick = tick

        logger.debug(
            "Time.set_datetime: set to %d/%d/%d %d:%d",
            self.year,
            self.month,
            self.day,
            self.hour,
            self.tick,
        )
