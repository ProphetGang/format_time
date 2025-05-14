import pytest

from time_engine.api import MoonCycleAPI, SunCycleAPI
from time_engine.moon_calendar import MoonCalendar
from time_engine.sun_calendar import SunCalendar
from time_engine.time import Time


@pytest.mark.integration
def test_time_to_api_query_consistency():
    """
    This test ensures that a valid Time configuration
    produces sun and moon tables whose values can be queried
    through the corresponding API consistently.
    """

    time_config = Time(
        ticks_per_hour=1,
        hours_per_day=24,
        days_per_month=30,
        months_per_year=12,
        lunar_cycle_days=360,
    )

    # Generate calendars
    sun = SunCalendar(time_config)
    moon = MoonCalendar(time_config)

    # Bind APIs
    sun_api = SunCycleAPI(sun.sun_table)
    moon_api = MoonCycleAPI(
        moon.moon_table, lunar_cycle_days=time_config.lunar_cycle_days
    )

    # Select key timestamps
    test_cases = [(0, 0), (10, 12), (100, 5), (359, 23)]

    for day, hour in test_cases:
        # Sun API matches table values
        assert sun_api.altitude(day, hour) == sun.sun_table[day, hour]

        # Moon API matches table values
        assert moon_api.altitude(day, hour) == moon.moon_table[day, hour]

        # Moon phase index is valid
        assert 0 <= moon_api.phase(day) <= 1
