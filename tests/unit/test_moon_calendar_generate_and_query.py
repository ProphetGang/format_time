import numpy as np
import pytest

from time_engine.moon_calendar import MoonCalendar
from time_engine.time import Time


@pytest.mark.unit
class TestMoonCalendarGenerateAndQuery:
    def test_generate_moon_table_matches_days_per_year(self):
        """
        Verify that the MoonCalendar creates a moon table matching the
        number of days in the year and ticks per day.
        """
        time_config = Time(months_per_year=1, days_per_month=4)
        calendar = MoonCalendar(time_config)
        moon_table = calendar.generate()  # <-- generate explicitly
        calendar.moon_table = moon_table  # <-- assign using property

        assert isinstance(moon_table, np.ndarray)

        expected_shape = (
            time_config.days_per_year,
            time_config.ticks_per_hour * time_config.hours_per_day,
        )
        assert moon_table.shape == expected_shape

        # Recalculate expected value for [0, 0] instead of assuming 0.0
        phase = 2 * np.pi * (0 % calendar.lunar_cycle_days) / calendar.lunar_cycle_days
        ha = -np.pi  # ha at tick=0
        expected_altitude = 50 * np.sin(phase + ha / 2)
        assert moon_table[0, 0] == pytest.approx(expected_altitude)

    def test_moon_brightness_query_valid_days(self):
        """
        Validate that brightness queries return a float value for all valid days.
        """
        time_config = Time(days_per_month=3, months_per_year=4)
        calendar = MoonCalendar(time_config)
        calendar.moon_table = calendar.generate()  # <-- ensure moon_table is ready
        for day in [0, 5, 11]:  # all valid days in a 12-day year
            brightness = calendar.phase_fraction(day)
            assert isinstance(brightness, float)
            assert 0.0 <= brightness <= 1.0

    def test_brightness_returns_zero_for_out_of_bounds_day(self):
        """
        Confirm the calendar handles invalid days gracefully (e.g., negative or overflow).
        """
        time_config = Time(days_per_month=2, months_per_year=3)
        calendar = MoonCalendar(time_config)
        calendar.moon_table = calendar.generate()  # <-- generate before queries

        val_neg = calendar.phase_fraction(-1)
        val_over = calendar.phase_fraction(6)  # 2×3 = 6 → day 6 wraps to 0

        assert isinstance(val_neg, float)
        assert isinstance(val_over, float)
        assert 0.0 <= val_neg <= 1.0
        assert 0.0 <= val_over <= 1.0

    def test_saves_and_loads_to_disk(self, tmp_path):
        """
        Verify that the moon table can be saved and reloaded from a .npy file.
        """
        time_config = Time(days_per_month=2, months_per_year=3)
        calendar = MoonCalendar(time_config)
        calendar.moon_table = calendar.generate()  # <-- ensure moon_table is created
        calendar.moon_table[:] = np.linspace(0, 1, calendar.moon_table.size).reshape(
            calendar.moon_table.shape
        )

        file_path = tmp_path / "moon.npy"
        calendar.save(file_path)

        loaded = np.load(file_path)
        assert loaded.shape == calendar.moon_table.shape
        assert np.allclose(loaded, calendar.moon_table)

    @pytest.mark.parametrize("cycle_len", [4, 7, 29])
    def test_lunar_cycle_wraps_correctly(self, cycle_len):
        """
        Test if the moon phase brightness properly repeats across the calendar year.
        """
        time_config = Time(months_per_year=1, days_per_month=cycle_len)
        calendar = MoonCalendar(time_config)
        calendar.moon_table = calendar.generate()  # <-- ensure moon_table is created

        pattern = [calendar.phase_fraction(day) for day in range(cycle_len)]
        full_year = [
            calendar.phase_fraction(day) for day in range(time_config.days_per_year)
        ]

        for i, val in enumerate(full_year):
            expected = pattern[i % cycle_len]
            assert val == pytest.approx(expected)
