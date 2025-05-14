import numpy as np
import pytest

from time_engine.moon_calendar import MoonCalendar
from time_engine.time import Time


@pytest.mark.module
class TestMoonCalendarModule:
    def test_generate_and_save_calendar(self, tmp_path):
        """
        Validate that the MoonCalendar:
        - Generates a 2D moon altitude table
        - Matches the expected shape
        - Saves and reloads correctly as a .npy file
        """
        time_config = Time(
            ticks_per_hour=1, hours_per_day=24, days_per_month=30, months_per_year=12
        )
        calendar = MoonCalendar(time_config)

        expected_shape = (
            time_config.days_per_year,
            time_config.ticks_per_hour * time_config.hours_per_day,
        )
        assert calendar.moon_table.shape == expected_shape

        assert np.all(np.isfinite(calendar.moon_table))  # sanity check for real numbers

        out_path = tmp_path / "moon_table.npy"
        calendar.save(out_path)

        assert out_path.exists()
        loaded = np.load(out_path)
        assert loaded.shape == expected_shape
        assert np.allclose(loaded, calendar.moon_table)

    def test_moon_altitude_lookup(self):
        """
        Confirm that the MoonCalendar returns a float value representing
        moon altitude for any valid (day, tick) pair.
        """
        time_config = Time()
        calendar = MoonCalendar(time_config)

        tick_count = time_config.ticks_per_hour * time_config.hours_per_day
        for day in [0, time_config.days_per_year // 2, time_config.days_per_year - 1]:
            for tick in [0, tick_count // 2, tick_count - 1]:
                altitude = calendar.altitude(day, tick)
                assert isinstance(altitude, float)
                assert -90.0 <= altitude <= 90.0  # reasonable altitude bounds
