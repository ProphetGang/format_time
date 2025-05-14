# tests/integration/test_unified_time_module_file_regeneration.py

import hashlib
import os
import time

import pytest

from parameters.manager import ParametersManager
from time_engine.unified_time_module import UnifiedTimeModule


def hash_file(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


@pytest.mark.integration
def test_hours_per_day_change_only_rebuilds_sun(tmp_path):
    """
    Changing hours_per_day should only regenerate the sun calendar file,
    leaving the moon calendar file untouched.
    """
    try:
        ParametersManager.reset()
    except AttributeError:
        pass

    data_dir = tmp_path / "calendar"
    params = ParametersManager()
    utm = UnifiedTimeModule(data_dir=str(data_dir), params=params)

    sun_path = data_dir / "sun_calendar.npy"
    moon_path = data_dir / "moon_calendar.npy"
    assert sun_path.exists() and moon_path.exists()

    sun_hash1 = hash_file(sun_path)
    moon_hash1 = hash_file(moon_path)

    old = int(params.get("time", "hours_per_day"))
    params.set("time", "hours_per_day", str(old + 1))

    time.sleep(0.1)

    sun_hash2 = hash_file(sun_path)
    moon_hash2 = hash_file(moon_path)

    assert sun_hash2 != sun_hash1, "Sun calendar should have been regenerated"
    assert moon_hash2 == moon_hash1, "Moon calendar should NOT have changed"


@pytest.mark.integration
def test_days_per_month_change_rebuilds_both(tmp_path):
    """
    Changing days_per_month should regenerate both sun and moon calendar files.
    """
    try:
        ParametersManager.reset()
    except AttributeError:
        pass

    data_dir = tmp_path / "calendar"
    params = ParametersManager()
    utm = UnifiedTimeModule(data_dir=str(data_dir), params=params)

    sun_path = data_dir / "sun_calendar.npy"
    moon_path = data_dir / "moon_calendar.npy"
    assert sun_path.exists() and moon_path.exists()

    sun_hash1 = hash_file(sun_path)
    moon_hash1 = hash_file(moon_path)

    old = int(params.get("time", "days_per_month"))
    params.set("time", "days_per_month", str(old + 1))

    time.sleep(0.1)

    sun_hash2 = hash_file(sun_path)
    moon_hash2 = hash_file(moon_path)

    assert sun_hash2 != sun_hash1, "Sun calendar should have been regenerated"
    assert moon_hash2 != moon_hash1, "Moon calendar should have been regenerated"
