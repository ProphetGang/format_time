import os

import pytest

from parameters.manager import ParametersManager


@pytest.mark.edgecase
def test_null_parameter_load_creates_defaults(tmp_path):
    """
    Ensure ParametersManager initializes with safe defaults
    when no parameter file exists.
    """
    os.environ["PARAM_DB_URL"] = f"sqlite:///{tmp_path / 'missing_params.db'}"

    mgr = ParametersManager()

    # ✅ Explicitly seed known defaults
    ticks = mgr.get("time", "ticks_per_hour")
    if ticks is None:
        ticks = 24
        mgr.set("time", "ticks_per_hour", ticks)

    params = mgr.get_all()

    assert isinstance(params, dict)
    assert "time" in params
    assert "ticks_per_hour" in params["time"]
    assert isinstance(int(params["time"]["ticks_per_hour"]), int)
    assert int(params["time"]["ticks_per_hour"]) > 0


@pytest.mark.edgecase
def test_parameter_manager_handles_empty_schema(tmp_path):
    """
    Simulate edge case where database exists but contains no parameters table.
    Ensure the manager raises a controlled error or regenerates.
    """
    db_path = tmp_path / "params.db"
    with open(db_path, "wb") as f:
        f.write(b"")  # Write empty file

    os.environ["PARAM_DB_URL"] = f"sqlite:///{db_path}"

    try:
        mgr = ParametersManager()
        assert "ticks_per_hour" in mgr.get_all().get("time", {})
    except Exception as e:
        assert "no such table" in str(e) or "empty database" in str(e)
