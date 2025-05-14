import pytest

from parameters.manager import ParametersManager
from time_engine.notification import NotificationManager


@pytest.mark.module
class TestManagerModule:
    def test_set_and_notify_cycle(self, monkeypatch):
        """
        Confirm that ParametersManager:
        - Stores values
        - Triggers notifications and local callbacks
        """
        notified = []

        # Allow real subscription logic but capture notify output
        original_notify = NotificationManager.notify

        def fake_notify(self, event, value=None):
            notified.append((event, value))
            original_notify(self, event, value)

        monkeypatch.setattr(NotificationManager, "notify", fake_notify)

        pm = ParametersManager()

        pm.on_change(
            "climate", "moisture", lambda v: notified.append(("local.moisture", v))
        )

        pm.set("climate", "moisture", 75)

        assert pm.get("climate", "moisture") == "75"
        assert ("climate.moisture", 75) in notified
        assert ("local.moisture", 75) in notified

    def test_values_persist_across_calls(self):
        """
        Ensure that values once set can be retrieved on new manager access (singleton pattern).
        """
        pm1 = ParametersManager()
        pm1.set("lighting", "sun_intensity", 42)

        pm2 = ParametersManager()

        assert pm2.get("lighting", "sun_intensity") == "42"
