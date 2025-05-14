import numpy as np
import pytest

from parameters.manager import ParametersManager
from time_engine.unified_time_module import UnifiedTimeModule


@pytest.mark.integration
def test_unified_time_module_regeneration_flow(tmp_path):
    """
    Validate that changing a time-related parameter triggers
    regeneration of the sun and moon tables in the UnifiedTimeModule.
    """

    # Set up test data directory and module
    data_dir = tmp_path / "calendar"
    params = ParametersManager()
    utm = UnifiedTimeModule(data_dir=str(data_dir), params=params)

    # Capture original state
    old_sun = utm.sun_table.copy()
    old_moon = utm.moon_table.copy()

    # Trigger a regeneration by changing a time parameter
    params.set("time", "days_per_month", 28)

    # UnifiedTimeModule listens to param changes and regenerates
    new_sun = utm.sun_table
    new_moon = utm.moon_table

    # Verify regeneration occurred
    assert new_sun.shape[0] != old_sun.shape[0], "Sun table was not regenerated."
    assert new_moon.shape[0] != old_moon.shape[0], "Moon table was not regenerated."

    # Optional: assert expected shape based on new time config
    expected_days = 28 * utm.time.months_per_year
    assert new_sun.shape[0] == expected_days
    assert new_moon.shape[0] == expected_days
