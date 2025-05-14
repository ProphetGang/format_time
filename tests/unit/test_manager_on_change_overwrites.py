import sys
from collections import defaultdict

import pytest

from parameters.manager import ParametersManager


class MockNotifier:
    """
    Pure in‐process pub/sub replacement that mimics NotificationManager.
    """

    def __init__(self):
        self._subs = defaultdict(list)  # ✅ Required to avoid KeyError

    def subscribe(self, event, callback):
        self._subs[event].append(callback)

    def notify(self, event, val=None):
        print(f"🚨 Notifying event: {event} with val={val}")
        for cb in self._subs[event]:
            print(f"➡️ Calling: {cb}")
            cb(val)

    def stop(self):
        self._subs.clear()


@pytest.mark.unit
def test_manager_on_change_overwrites():
    calls = []

    # 🧼 Reset ParametersManager
    ParametersManager.reset()

    # ✅ Inject compatible mock notifier
    mock_notifier = MockNotifier()
    pm = ParametersManager(notifier=mock_notifier)

    # 🧪 Confirm injection consistency
    print("Injected Notifier ID:", id(mock_notifier))
    print("PM Notifier ID:      ", id(pm._notifier))

    # 🔁 Register two callbacks to the same event
    pm.on_change("display", "contrast", lambda v: calls.append(("first", v)))
    pm.on_change("display", "contrast", lambda v: calls.append(("second", v)))

    # 🧪 Print subscriptions for confirmation
    print("Subscribed Events:", list(mock_notifier._subs.keys()))

    # ⚠️ Set a different value first to ensure `notify` triggers
    pm.set("display", "contrast", 5)

    # 🚀 Trigger event: this time it’s a real change
    print("Before value:", pm.get("display", "contrast"))
    pm.set("display", "contrast", 10)
    print("After value:", pm.get("display", "contrast"))

    print("CALLS:", calls)

    # ✅ Only assert the final expected calls
    assert calls[-2:] == [("first", 10), ("second", 10)]
