# tests/integration/test_notification_sent_on_time_change.py

import time

import pytest

from parameters.manager import ParametersManager
from time_engine.notification import NotificationManager
from time_engine.unified_time_module import UnifiedTimeModule


@pytest.mark.integration
def test_notification_sent_on_time_change():
    """
    Verify that changing a time-related parameter causes the
    NotificationManager to send a message (simulated broadcast).
    """
    sent_packets = []

    def capture(value):
        sent_packets.append(value)

    # Reset both NotificationManager and ParametersManager
    NotificationManager._instance = None
    ParametersManager.reset()

    # Inject shared notifier into ParametersManager and UnifiedTimeModule
    shared_notifier = NotificationManager()
    shared_notifier.reset()  # ← Added reset of the in-memory queue/thread
    pm = ParametersManager(notifier=shared_notifier)

    # Subscribe through the manager's API to ensure internal linkage
    pm.on_change("time", "ticks_per_hour", capture)

    utm = UnifiedTimeModule(data_dir="calendar_test_dir", params=pm)

    # Force a value change to trigger notify()
    original = pm.get("time", "ticks_per_hour")
    new_val = str(int(original) + 1 if original else 999)
    pm.set("time", "ticks_per_hour", new_val)

    # Allow background dispatch to run
    time.sleep(0.1)

    assert sent_packets, "No notification was sent."
    assert sent_packets[0] in (new_val, int(new_val))
