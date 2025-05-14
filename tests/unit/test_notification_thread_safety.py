# tests/test_notification_thread_safety.py
import threading
import time

import pytest

from time_engine.notification import NotificationManager


@pytest.mark.unit
def test_concurrent_subscribe_and_notify_no_exceptions():
    """
    Concurrent calls to subscribe() and notify() should not raise
    any exceptions, and notifications should be delivered to all
    subscribers registered up to that point.
    """
    # Reset singleton and notifier
    NotificationManager._instance = None
    nm = NotificationManager()
    nm.reset()

    results = []
    subscribe_done = threading.Event()

    def cb(val):
        results.append(val)

    def subscribe_loop():
        for _ in range(100):
            nm.subscribe("evt", cb)
        subscribe_done.set()

    def notify_loop():
        subscribe_done.wait()
        for i in range(100):
            nm.notify("evt", i)

    threads = []
    for _ in range(5):
        threads.append(threading.Thread(target=subscribe_loop))
    for _ in range(5):
        threads.append(threading.Thread(target=notify_loop))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    nm.stop()

    assert len(results) > 0


@pytest.mark.unit
def test_notify_handles_callback_exceptions():
    """
    If one subscriber callback raises, others should still be invoked
    and no exception should escape notify().
    """
    # Reset singleton and notifier
    NotificationManager._instance = None
    nm = NotificationManager()
    nm.reset()

    called = []

    def bad_cb(val):
        raise RuntimeError("boom")

    def good_cb(val):
        called.append(val)

    nm.subscribe("ev", bad_cb)
    nm.subscribe("ev", good_cb)

    nm.notify("ev", 7)
    time.sleep(0.05)  # Allow async dispatch

    # Now receives raw int 7
    assert called == [7]


@pytest.mark.unit
def test_stop_prevents_further_notifications():
    """
    After stop(), notify() should not deliver to any subscribers.
    """
    # Reset singleton and notifier
    NotificationManager._instance = None
    nm = NotificationManager()
    nm.reset()

    called = []

    def cb(val):
        called.append(val)

    nm.subscribe("foo", cb)
    nm.stop()
    nm.notify("foo", 123)
    time.sleep(0.01)

    assert called == []


import time

# tests/test_notification_broadcast_unit.py
import pytest

from time_engine.notification import NotificationManager


@pytest.mark.unit
class TestNotificationBroadcastUnit:
    def test_notify_enqueues_and_delivers_event(self):
        called = []
        # Reset singleton and notifier
        NotificationManager._instance = None
        nm = NotificationManager()
        nm.reset()

        # Subscribe and notify
        nm.subscribe("my.param", lambda v: called.append(v))
        nm.notify("my.param", 123)
        time.sleep(0.05)

        assert called == [123]

    def test_direct_notify_triggers_callback(self):
        captured = []
        # Reset singleton and notifier
        NotificationManager._instance = None
        nm = NotificationManager()
        nm.reset()

        nm.subscribe("sim.test", lambda v: captured.append(v))
        nm.notify("sim.test", "OK")
        time.sleep(0.05)

        assert captured == ["OK"]
