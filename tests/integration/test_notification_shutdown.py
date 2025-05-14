# tests/integration/test_notification_shutdown.py

import time

import pytest

from time_engine.notification import NotificationManager


@pytest.mark.integration
def test_notification_manager_shutdown_prevents_further_delivery():
    """
    After calling stop(), the dispatcher thread should exit and
    no further notifications (including direct ones) should be delivered.
    """
    # Ensure fresh singleton & notifier
    NotificationManager._instance = None
    manager = NotificationManager()
    manager.reset()

    received = []

    # Subscribe a handler
    manager.subscribe("shutdown.test", lambda v: received.append(v))

    # Stop the manager (should terminate dispatcher and disable further delivery)
    manager.stop()

    # Give a moment for the dispatcher thread to terminate
    time.sleep(0.1)

    # Dispatcher thread should no longer be alive
    assert not manager._thread.is_alive(), "Dispatcher thread did not stop"

    # Attempt to send a notification (bypasses UDP but still uses notify)
    manager.notify("shutdown.test", 123)
    time.sleep(0.05)

    # Since stopped, no callbacks should be invoked
    assert received == []
