import pytest

from time_engine.moon_calendar import MoonCalendar
from time_engine.time import Time


@pytest.mark.edgecase
def test_moon_brightness_stays_within_bounds():
    """
    Validates that all moon brightness values remain in the [0.0, 1.0] range,
    even for large or unusual calendar configurations.
    """
    # Simulate a long calendar with many days to stress the phase computation
    time_config = Time(
        ticks_per_hour=1,
        hours_per_day=24,
        days_per_month=30,
        months_per_year=12,
        lunar_cycle_days=29,  # standard lunar cycle
    )
    moon = MoonCalendar(time_config)

    for day in range(time_config.days_per_year):
        brightness = moon.brightness(day)
        assert (
            0.0 <= brightness <= 1.0
        ), f"Day {day} brightness out of bounds: {brightness}"
