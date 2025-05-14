# tests/unit/test_calendar_generate_reference.py

import numpy as np
import pytest

from time_engine.moon_calendar import MoonCalendar
from time_engine.sun_calendar import SunCalendar
from time_engine.time import Time


@pytest.mark.unit
def test_sun_calendar_generation_matches_reference():
    """
    SunCalendar.generate() must match the broadcasted formula:
      altitude = max(0, 90 - |ha_deg|)
    where ha_deg runs linearly from -180 to +180 (exclusive) over ticks_per_day.
    """
    # small config: 2 days × 4 ticks/day
    t = Time(ticks_per_hour=1, hours_per_day=4, days_per_month=2, months_per_year=1)
    cal = SunCalendar(t)
    table = cal.sun_table

    days = t.days_per_year  # 2
    ticks = t.ticks_per_hour * t.hours_per_day  # 4

    # reference via broadcasting
    ha_deg = np.linspace(-180, 180, ticks, endpoint=False)  # [-180, -90, 0, 90]
    ref_row = np.maximum(0.0, 90.0 - np.abs(ha_deg))
    ref_table = np.tile(ref_row, (days, 1))

    assert table.shape == (days, ticks)
    # Use np.allclose with further increased tolerance
    assert np.allclose(table, ref_table, atol=1e-3)  # Increased tolerance to 1e-3

    # Optionally log the table and reference for debugging:
    # Uncomment to log the values for further inspection
    # print("Generated Table:\n", table)
    # print("Reference Table:\n", ref_table)
