import os

import pytest

from time_engine.unified_time_module import UnifiedTimeModule


@pytest.mark.integration
def test_unified_time_module_honors_custom_data_dir(tmp_path):
    """
    UnifiedTimeModule(data_dir=...) must write both calendars
    under that directory, and not in the default package data folder.
    """
    custom = tmp_path / "my_cal"
    utm = UnifiedTimeModule(data_dir=str(custom))

    # Force generation
    utm.rebuild_calendars()

    sun_file = custom / "sun_calendar.npy"
    moon_file = custom / "moon_calendar.npy"
    assert sun_file.exists(), f"Expected sun calendar at {sun_file}"
    assert moon_file.exists(), f"Expected moon calendar at {moon_file}"

    # There should be no calendars in the legacy default path
    default_dir = os.path.join(
        os.path.dirname(__file__), os.pardir, "time_engine", "data"
    )
    assert not os.path.exists(default_dir), "Default data dir should not be used"
