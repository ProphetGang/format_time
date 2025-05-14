import sys

import numpy as np
import pytest

from time_engine import clock


@pytest.mark.unit
class TestClockMainUnit:
    def test_time_advancement_prints_datetime(self, monkeypatch, capsys):
        monkeypatch.setattr(sys, "argv", ["clock.py", "--ticks", "48"])
        clock.main()
        captured = capsys.readouterr()
        assert "Year:" in captured.out
        assert "Tick:" in captured.out

    def test_sun_calendar_generation_prints_success(self, monkeypatch, capsys):
        monkeypatch.setattr(sys, "argv", ["clock.py", "--generate-sun-calendar"])
        monkeypatch.setattr(
            "time_engine.sun_calendar.SunCalendar.save", lambda self, path: None
        )
        clock.main()
        captured = capsys.readouterr()
        assert "Sun calendar written" in captured.out

    def test_moon_calendar_generation_prints_success(self, monkeypatch, capsys):
        monkeypatch.setattr(sys, "argv", ["clock.py", "--generate-moon-calendar"])
        monkeypatch.setattr(
            "time_engine.moon_calendar.MoonCalendar.save", lambda self, path: None
        )
        clock.main()
        captured = capsys.readouterr()
        assert "Moon calendar written" in captured.out

    def test_sun_altitude_query_prints_result(self, monkeypatch, capsys):
        monkeypatch.setattr(sys, "argv", ["clock.py", "--sun-altitude", "1", "2"])
        dummy = np.ones((5, 5)) * 45.0
        monkeypatch.setattr(np, "load", lambda path: dummy)
        clock.main()
        captured = capsys.readouterr()
        assert "Sun altitude" in captured.out

    def test_moon_phase_query_prints_result(self, monkeypatch, capsys):
        monkeypatch.setattr(sys, "argv", ["clock.py", "--moon-phase", "3"])
        dummy = np.ones((4, 3))  # ✅ 2D shape: (days_per_year, ticks_per_day)
        monkeypatch.setattr(np, "load", lambda path: dummy)
        clock.main()
        captured = capsys.readouterr()
        assert "Moon phase" in captured.out
