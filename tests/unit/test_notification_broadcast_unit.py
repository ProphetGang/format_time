# tests/test_notification_broadcast_unit.py

import time

import pytest

from time_engine.notification import NotificationManager


@pytest.mark.unit
class TestNotificationBroadcastUnit:
    def test_notify_enqueues_and_delivers_event(self):
        called = []
        NotificationManager._instance = None
        nm = NotificationManager()
        nm.reset()

        nm.subscribe("my.param", lambda v: called.append(v))
        nm.notify("my.param", 123)
        time.sleep(0.05)

        assert called == [123]

    def test_direct_notify_triggers_callback(self):
        captured = []
        NotificationManager._instance = None
        nm = NotificationManager()
        nm.reset()

        nm.subscribe("sim.test", lambda v: captured.append(v))
        nm.notify("sim.test", "OK")
        time.sleep(0.05)

        assert captured == ["OK"]
