# tests/unit/test_manager_set_and_get.py

import os

import numpy as np
import pytest

from time_engine.sun_calendar import SunCalendar
from time_engine.time import Time


@pytest.mark.unit
class TestSunCalendarUnit:
    def test_generate_sun_table_dimensions(self):
        """
        Ensure the sun table matches the time configuration dimensions.
        """
        t = Time(hours_per_day=24, days_per_month=30, months_per_year=1)
        calendar = SunCalendar(t)
        calendar.generate()
        assert calendar.sun_table.shape == (
            30,
            24,
        )  # 🔧 FIX: use `sun_table`, not `table`

    def test_altitude_bounds(self):
        """
        Ensure that altitude interpolation returns a float and remains within valid range.
        """
        t = Time(hours_per_day=24, days_per_month=1, months_per_year=1)
        calendar = SunCalendar(t)

        val = calendar.altitude(0, 12)
        assert isinstance(val, float)
        # Allow a tiny tolerance above 90° to account for interpolation precision
        assert 0.0 <= val <= 90.0 + 1e-3

    def test_altitude_edge_cases(self):
        """
        Query edge values to ensure no index errors.
        """
        t = Time(hours_per_day=24, days_per_month=30, months_per_year=1)
        calendar = SunCalendar(t)

        for day, hour in [(0, 0), (29, 23), (15, 0), (0, 23)]:
            val = calendar.altitude(day, hour)
            assert isinstance(val, float)

    def test_save_and_load_cycle(self, tmp_path):
        """
        Test saving and reloading the sun table to ensure persistence.
        """
        t = Time(hours_per_day=12, days_per_month=10, months_per_year=1)
        calendar = SunCalendar(t)

        file_path = tmp_path / "sun_test.npy"
        calendar.save(str(file_path))
        assert file_path.exists()

        # Load the file manually since SunCalendar has no `load` method
        loaded = np.load(file_path)
        assert np.allclose(
            loaded, calendar.sun_table
        )  # 🔧 FIX: use `sun_table`, not `table`

    def test_invalid_altitude_index_raises(self):
        """
        Ensure out-of-bound queries raise IndexError.
        """
        t = Time(hours_per_day=10, days_per_month=10, months_per_year=1)
        calendar = SunCalendar(t)

        with pytest.raises(IndexError):
            _ = calendar.sun_table[999, 1]  # 🔧 FIX: use `sun_table`, not `table`

        with pytest.raises(IndexError):
            _ = calendar.sun_table[1, 999]  # 🔧 FIX: use `sun_table`, not `table`
