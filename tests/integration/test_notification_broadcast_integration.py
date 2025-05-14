# tests/test_notification_broadcast_integration.py

import time

import pytest

from time_engine.notification import NotificationManager


@pytest.mark.integration
class TestNotificationBroadcastIntegration:
    def test_subscribe_and_receive_callback(self):
        captured = {}

        def handler(val):
            captured["value"] = val

        # Reset singleton and notifier
        NotificationManager._instance = None
        manager = NotificationManager()
        manager.reset()

        # Subscribe and fire directly
        manager.subscribe("foo.bar", handler)
        manager.notify("foo.bar", "42")

        # Wait for delivery from dispatcher thread
        timeout = time.time() + 1.0
        while "value" not in captured and time.time() < timeout:
            time.sleep(0.05)

        manager.stop()

        assert "value" in captured
        assert captured["value"] == "42"
