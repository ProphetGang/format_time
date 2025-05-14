import pytest

from parameters.manager import ParametersManager
from time_engine.notification import NotificationManager


@pytest.mark.unit
def test_manager_notify(monkeypatch):
    notified = []

    def fake_notify(self, event, val=None):
        notified.append((event, val))

    monkeypatch.setattr(NotificationManager, "notify", fake_notify)

    pm = ParametersManager()
    pm.set("world", "humidity", 55)

    assert ("world.humidity", 55) in notified
