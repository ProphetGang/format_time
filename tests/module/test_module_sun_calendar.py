import numpy as np
import pytest

from time_engine.sun_calendar import SunCalendar
from time_engine.time import Time


@pytest.mark.module
class TestSunCalendarModule:
    def test_generate_and_save_calendar(self, tmp_path):
        """
        Validate that the SunCalendar:
        - Generates a correct calendar table
        - Matches time configuration (days × ticks)
        - Saves to disk as a .npy file and reloads correctly
        """
        time_config = Time(
            ticks_per_hour=2,
            hours_per_day=24,
            days_per_month=30,
            months_per_year=12,
        )
        calendar = SunCalendar(time_config)

        expected_days = time_config.days_per_year
        expected_ticks = time_config.ticks_per_hour * time_config.hours_per_day
        assert calendar.sun_table.shape == (expected_days, expected_ticks)

        out_path = tmp_path / "sun_table.npy"
        calendar.save(out_path)
        assert out_path.exists()

        loaded = np.load(out_path)
        assert loaded.shape == (expected_days, expected_ticks)
        assert np.allclose(loaded, calendar.sun_table)

    def test_sun_altitude_interpolation(self):
        """
        Confirm that the calendar returns correct sun altitude
        when requested by [day, tick].
        """
        time_config = Time()
        calendar = SunCalendar(time_config)

        tick = 12 * time_config.ticks_per_hour  # tick index at noon
        altitude = calendar.altitude(day=10, tick=tick)
        assert isinstance(altitude, float)
        assert 0.0 <= altitude <= 90.0
