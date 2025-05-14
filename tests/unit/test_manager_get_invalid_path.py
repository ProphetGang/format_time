import pytest

from parameters.manager import ParametersManager


@pytest.mark.unit
def test_manager_get_invalid_path():
    pm = ParametersManager()
    pm.set("a", "b", 42)

    # Should return None or fallback, but not crash
    assert pm.get("a", "missing") is None
    assert pm.get("not", "present", default="x") == "x"
