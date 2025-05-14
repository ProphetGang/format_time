import os

import numpy as np
import pytest

from time_engine.moon_calendar import MoonCalendar
from time_engine.sun_calendar import SunCalendar
from time_engine.time import Time


@pytest.mark.edgecase
def test_suncalendar_save_tmp_corrupted_then_fallback(tmp_path, monkeypatch):
    target = tmp_path / "sun.npy"
    tmp_target = str(target) + ".tmp"

    # Create calendar and manually write a leftover .tmp file
    cal = SunCalendar(Time(hours_per_day=1, days_per_month=1, months_per_year=1))
    np.save(tmp_target, cal.sun_table)

    # Now patch os.replace to simulate failure ONLY on this call
    def fake_replace(src, dst):
        raise OSError("simulated replace failure")

    monkeypatch.setattr("time_engine.sun_calendar.os.replace", fake_replace)

    # Expect fallback recovery to fail due to simulated replace
    with pytest.raises(OSError):
        cal.ensure(str(target))

    # Restore real replace for fallback recovery
    monkeypatch.undo()

    # Now retry: ensure should recover from .tmp
    cal.ensure(str(target))
    assert target.exists()


@pytest.mark.edgecase
def test_mooncalendar_save_tmp_corrupted_then_fallback(tmp_path, monkeypatch):
    target = tmp_path / "moon.npy"
    tmp_target = str(target) + ".tmp"

    cal = MoonCalendar(Time(days_per_month=1, months_per_year=1))
    np.save(tmp_target, cal.moon_table)

    def fake_replace(src, dst):
        raise OSError("simulated replace failure")

    monkeypatch.setattr("time_engine.moon_calendar.os.replace", fake_replace)

    with pytest.raises(OSError):
        cal.ensure(str(target))

    monkeypatch.undo()

    cal.ensure(str(target))
    assert target.exists()
