from pathlib import Path

import numpy as np
import pytest

from parameters.manager import ParametersManager
from time_engine.unified_time_module import UnifiedTimeModule


@pytest.mark.integration
def test_manager_on_change_to_unified_time(tmp_path):
    """
    When time-related parameters are updated via ParametersManager,
    UnifiedTimeModule should respond by regenerating internal structures
    like the sun/moon calendar tables.
    """

    # Setup clean environment
    param_db_path = tmp_path / "params.db"
    data_dir = tmp_path / "calendar"
    data_dir.mkdir(exist_ok=True)

    # ✅ Use the PARAM_DB_PATH env var so UnifiedTimeModule reads it
    import os

    os.environ["PARAM_DB_PATH"] = str(param_db_path)

    # Instantiate the module — it will internally use ParametersManager
    module = UnifiedTimeModule(data_dir=str(data_dir))

    # Capture the original sun table
    original_sun = module.sun_table.copy()

    # ✅ Use ParametersManager to update a value
    pm = ParametersManager()
    pm.set("time", "ticks_per_hour", "42")  # must be string

    # ✅ Let the system hook update kick in
    import time

    timeout = time.time() + 1.0
    while np.array_equal(module.sun_table, original_sun) and time.time() < timeout:
        time.sleep(0.05)

    # ✅ Calculate expected new shape
    expected_shape = (
        module.time.days_per_year,
        module.time.hours_per_day * module.time.ticks_per_hour,
    )

    # ✅ Assertions
    assert (
        module.sun_table.shape == expected_shape
    ), f"Expected shape {expected_shape}, got {module.sun_table.shape}"
    assert not np.array_equal(
        module.sun_table, original_sun
    ), "Sun table was not regenerated after parameter update"
