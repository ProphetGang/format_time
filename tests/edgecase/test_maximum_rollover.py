import pytest

from time_engine.time import Time


@pytest.mark.edgecase
def test_time_massive_rollover_boundary():
    t = Time(ticks_per_hour=1, hours_per_day=24, days_per_month=30, months_per_year=12)
    one_million_ticks = 1_000_000
    t.advance(one_million_ticks)

    dt = t.current_datetime()

    # Should still give valid structure
    assert 1 <= dt["month"] <= 12
    assert 1 <= dt["day"] <= 30
    assert 0 <= dt["hour"] < 24
