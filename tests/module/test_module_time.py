import pytest

from time_engine.time import Time


@pytest.mark.module
class TestTimeModule:
    def test_full_year_rollover(self):
        time = Time(
            ticks_per_hour=1, hours_per_day=24, days_per_month=30, months_per_year=12
        )
        total_ticks = (
            time.ticks_per_hour
            * time.hours_per_day
            * time.days_per_month
            * time.months_per_year
        )
        time.advance(total_ticks)
        dt = time.current_datetime()
        assert dt["year"] == 2
        assert dt["month"] == 1
        assert dt["day"] == 1
        assert dt["hour"] == 0
        assert dt["tick"] == 0

    def test_day_rollover(self):
        time = Time(ticks_per_hour=1, hours_per_day=24, days_per_month=30)
        ticks_to_advance = 24  # 1 full day
        time.advance(ticks_to_advance)
        dt = time.current_datetime()
        assert dt["day"] == 2
        assert dt["hour"] == 0
        assert dt["tick"] == 0

    def test_month_rollover(self):
        time = Time(ticks_per_hour=1, hours_per_day=24, days_per_month=2)
        ticks_to_advance = 2 * 24  # 2 days -> 1 month rollover
        time.advance(ticks_to_advance)
        dt = time.current_datetime()
        assert dt["month"] == 2
        assert dt["day"] == 1

    def test_multiple_rollovers(self):
        time = Time(
            ticks_per_hour=2, hours_per_day=10, days_per_month=2, months_per_year=3
        )
        # Advance 120 ticks: should cause full rollover into Year 2
        time.advance(120)
        dt = time.current_datetime()
        assert dt["year"] == 2
        assert dt["month"] == 1
        assert dt["day"] == 1
        assert dt["hour"] == 0
        assert dt["tick"] == 0
