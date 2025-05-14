import pytest

from parameters.manager import ParametersManager
from time_engine.notification import NotificationManager


@pytest.mark.unit
def test_manager_skip_notify_if_value_unchanged(monkeypatch):
    triggered = []

    def fake_notify(self, event, val=None):
        triggered.append((event, val))

    monkeypatch.setattr(NotificationManager, "notify", fake_notify)

    pm = ParametersManager()
    pm.set("graphics", "shadows", True)
    pm.set("graphics", "shadows", True)  # should NOT trigger

    assert triggered == [("graphics.shadows", True)]
