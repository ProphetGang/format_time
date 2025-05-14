from pathlib import Path

import numpy as np
import pytest

from time_engine.time import Time
from time_engine.unified_time_module import UnifiedTimeModule


@pytest.mark.unit
class TestUnifiedTimeModule:
    def test_initialization_creates_default_time_and_paths(self, tmp_path):
        module = UnifiedTimeModule(data_dir=str(tmp_path))
        assert isinstance(module.time, Time)
        assert "sun_calendar.npy" in str(module.sun_path)
        assert "moon_calendar.npy" in str(module.moon_path)

    def test_rebuild_calendars_creates_and_saves_tables(self, tmp_path, monkeypatch):
        save_calls = {"sun": False, "moon": False}

        class DummySunCalendar:
            def __init__(self, time):
                pass

            def save(self, path):
                save_calls["sun"] = Path(path).name == "sun_calendar.npy"
                np.save(path, np.full((10, 10), 42.0))

            def get_table(self):
                return np.full((10, 10), 42.0)

        class DummyMoonCalendar:
            def __init__(self, time):
                pass

            def save(self, path):
                save_calls["moon"] = Path(path).name == "moon_calendar.npy"
                np.save(path, np.full((10, 1), 0.5))

            def get_table(self):
                return np.full((10, 1), 0.5)

        monkeypatch.setattr(
            "time_engine.unified_time_module.SunCalendar", DummySunCalendar
        )
        monkeypatch.setattr(
            "time_engine.unified_time_module.MoonCalendar", DummyMoonCalendar
        )

        module = UnifiedTimeModule(data_dir=str(tmp_path))
        module.rebuild_calendars()

        assert np.all(module.sun_table == 42.0)
        assert np.all(module.moon_table == 0.5)
        assert save_calls["sun"]
        assert save_calls["moon"]

    def test_ensure_calendars_loads_existing(self, tmp_path):
        # Setup fake tables
        sun_path = tmp_path / "sun_calendar.npy"
        moon_path = tmp_path / "moon_calendar.npy"
        np.save(sun_path, np.array([[1.0]]))
        np.save(moon_path, np.array([0.1]))

        module = UnifiedTimeModule(data_dir=str(tmp_path))
        assert isinstance(module.sun_table, np.ndarray)
        assert isinstance(module.moon_table, np.ndarray)

    def test_on_param_change_triggers_calendar_reload(self, tmp_path, monkeypatch):
        reload_flag = {"called": False}

        def dummy_rebuild(self):
            reload_flag["called"] = True
            self.sun_table = np.ones((1, 1))
            self.moon_table = np.zeros((1,))

        monkeypatch.setattr(
            "time_engine.unified_time_module.UnifiedTimeModule.rebuild_calendars",
            dummy_rebuild,
        )

        module = UnifiedTimeModule(data_dir=str(tmp_path))
        module._on_param_change("time.days_per_month", 31)

        assert reload_flag["called"]
        assert isinstance(module.sun_table, np.ndarray)
