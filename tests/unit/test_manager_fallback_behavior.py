import pytest

from parameters.manager import ParametersManager


@pytest.mark.unit
def test_manager_fallback_behavior():
    pm = ParametersManager()
    assert pm.get("nonexistent", "key", default=123) == 123
    assert pm.get("still.none", "missing") is None
