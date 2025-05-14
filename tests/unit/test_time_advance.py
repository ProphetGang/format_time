import logging

logger = logging.getLogger(__name__)


class Time:
    def __init__(
        self,
        *,
        ticks_per_hour=1,
        hours_per_day=24,
        days_per_month=30,
        months_per_year=12,
        lunar_cycle_days=None
    ):
        self.ticks_per_hour = ticks_per_hour
        self.hours_per_day = hours_per_day
        self.days_per_month = days_per_month
        self.months_per_year = months_per_year
        self.lunar_cycle_days = lunar_cycle_days or (days_per_month * months_per_year)
        self.ticks = 0
        self.hour = 0
        self.day = 1
        self.month = 1
        self.year = 1

    def advance(self, delta_ticks: int):
        """
        Advance the timeline by `delta_ticks`. Handles rollover
        at each unit and logs checkpoint messages.
        """
        # increment raw ticks
        self.ticks += delta_ticks

        # ticks → hours
        hours_advance, self.ticks = divmod(self.ticks, self.ticks_per_hour)
        self.hour += hours_advance
        if hours_advance:
            logger.debug("checkpoint: advance:hour_rollover")

        # hours → days
        days_advance, self.hour = divmod(self.hour, self.hours_per_day)
        self.day += days_advance
        if days_advance:
            logger.debug("checkpoint: advance:day_rollover")

        # days → months
        # note: days are 1-indexed internally
        months_advance, day_index = divmod(self.day - 1, self.days_per_month)
        self.day = day_index + 1
        self.month += months_advance
        if months_advance:
            logger.debug("checkpoint: advance:month_rollover")

        # months → years
        years_advance, month_index = divmod(self.month - 1, self.months_per_year)
        self.month = month_index + 1
        self.year += years_advance
        if years_advance:
            logger.debug("checkpoint: advance:year_rollover")

        # Final summary log
        logger.debug(
            "Time.advance: +%d tick(s) → +%d hour(s), +%d day(s), +%d month(s), +%d year(s); now %d/%d/%d %d:%d",
            delta_ticks,
            hours_advance,
            days_advance,
            months_advance,
            years_advance,
            self.year,
            self.month,
            self.day,
            self.hour,
            self.ticks,
        )

    def current_datetime(self):
        """Return current time as a dict."""
        return {
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "hour": self.hour,
            "tick": self.ticks,
        }
