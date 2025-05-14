import hashlib
import logging
import os
import time

import pytest

from parameters.manager import ParametersManager
from time_engine.unified_time_module import UnifiedTimeModule

# 🔧 Enable full debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s [%(name)s:%(lineno)d] %(message)s",
)

logger = logging.getLogger(__name__)


def hash_file(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


@pytest.mark.integration
def test_hours_per_day_change_only_rebuilds_sun(tmp_path):
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
    logger.debug("✅ Initial hashes: sun=%s, moon=%s", sun_hash1, moon_hash1)

    old = int(params.get("time", "hours_per_day"))
    logger.debug("🔁 Changing hours_per_day from %d to %d", old, old + 1)
    params.set("time", "hours_per_day", str(old + 1))
    params._notifier.notify("time.hours_per_day", str(old + 1))

    time.sleep(0.5)

    sun_hash2 = hash_file(sun_path)
    moon_hash2 = hash_file(moon_path)
    logger.debug("✅ Post-change hashes: sun=%s, moon=%s", sun_hash2, moon_hash2)

    print("✅ Before change:")
    print(f"    sun_hash = {sun_hash1}")
    print(f"    moon_hash = {moon_hash1}")
    print("✅ After change:")
    print(f"    sun_hash = {sun_hash2}")
    print(f"    moon_hash = {moon_hash2}")

    assert sun_hash2 != sun_hash1, "Sun calendar should have been regenerated"
    assert moon_hash2 == moon_hash1, "Moon calendar should NOT have changed"


@pytest.mark.integration
def test_days_per_month_change_rebuilds_both(tmp_path):
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
    logger.debug("✅ Initial hashes: sun=%s, moon=%s", sun_hash1, moon_hash1)

    old = int(params.get("time", "days_per_month"))
    logger.debug("🔁 Changing days_per_month from %d to %d", old, old + 1)
    params.set("time", "days_per_month", str(old + 1))
    params._notifier.notify("time.days_per_month", str(old + 1))

    time.sleep(0.5)

    sun_hash2 = hash_file(sun_path)
    moon_hash2 = hash_file(moon_path)
    logger.debug("✅ Post-change hashes: sun=%s, moon=%s", sun_hash2, moon_hash2)

    print("✅ Before change:")
    print(f"    sun_hash = {sun_hash1}")
    print(f"    moon_hash = {moon_hash1}")
    print("✅ After change:")
    print(f"    sun_hash = {sun_hash2}")
    print(f"    moon_hash = {moon_hash2}")

    assert sun_hash2 != sun_hash1, "Sun calendar should have been regenerated"
    assert moon_hash2 != moon_hash1, "Moon calendar should have been regenerated"
