import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import os

import pytest

from parameters.manager import ParametersManager
from time_engine.moon_calendar import MoonCalendar
from time_engine.notification import NotificationManager
from time_engine.sun_calendar import SunCalendar
from time_engine.time import Time
from time_engine.unified_time_module import UnifiedTimeModule


@pytest.fixture(autouse=True)
def clean_parameters(tmp_path, monkeypatch):
    """
    Provides a clean in-memory parameter database.
    Automatically resets singleton for ParametersManager.
    """
    db_path = tmp_path / "params.db"
    monkeypatch.setenv("PARAM_DB_PATH", str(db_path))

    # Full reset of singleton and callback state
    try:
        ParametersManager.reset()
    except AttributeError:
        pass

    pm = ParametersManager(db_url=f"sqlite:///{db_path}")
    return pm


@pytest.fixture
def temp_time_config():
    config = Time(
        ticks_per_hour=2, hours_per_day=24, days_per_month=30, months_per_year=12
    )
    return config


@pytest.fixture
def sun_calendar(temp_time_config):
    calendar = SunCalendar(temp_time_config)
    return calendar


@pytest.fixture
def moon_calendar(temp_time_config):
    calendar = MoonCalendar(temp_time_config)
    return calendar


@pytest.fixture
def time_module(tmp_path):
    """
    Returns a clean UnifiedTimeModule instance with isolated calendar storage.
    """
    data_dir = tmp_path / "calendar_data"
    data_dir.mkdir(parents=True, exist_ok=True)
    utm = UnifiedTimeModule(data_dir=str(data_dir))
    return utm


@pytest.fixture
def notification_manager():
    nm = NotificationManager()
    return nm


@pytest.fixture
def dummy_calendar_table():
    """
    Returns a small 2D numpy array for sun/moon table mocking.
    """
    import numpy as np

    arr = np.array([[10.0, 20.0], [30.0, 40.0]])
    return arr


@pytest.fixture
def disable_socket(monkeypatch):
    """
    Disables real socket behavior during broadcast tests.
    """
    import socket

    class DummySocket:
        def setsockopt(self, *_):
            pass

        def settimeout(self, *_):
            pass

        def bind(self, *_):
            pass

        def recvfrom(self, *_):
            return b"", None

        def sendto(self, *_):
            return None

        def close(self):
            pass

    monkeypatch.setattr(socket, "socket", lambda *_: DummySocket())
