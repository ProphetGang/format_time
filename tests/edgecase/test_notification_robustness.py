# tests/edgecase/test_notification_robustness.py
import time

import pytest

from time_engine.notification import NotificationManager


@pytest.mark.edgecase
def test_notification_callback_exception_does_not_block():
    # 🔄 Ensure fresh instance
    NotificationManager._instance = None
    nm = NotificationManager()
    nm.reset()

    calls = []

    def bad_cb(val):
        raise RuntimeError("boom")

    def good_cb(val):
        calls.append(val)

    # 🛠 Subscribe both a bad and a good callback
    nm.subscribe("ev.test", bad_cb)
    nm.subscribe("ev.test", good_cb)

    # 🚀 Fire a notification
    nm.notify("ev.test", 7)
    time.sleep(0.05)  # allow async dispatch
    nm.stop()

    # ✅ Only the good callback ran, and we got the raw int back
    assert calls == [7]
