# tests/edgecase/test_notifcation_fails_silently.py
import pytest

from time_engine.notification import NotificationManager


@pytest.mark.edgecase
def test_notification_queue_failure_is_handled(monkeypatch):
    class BrokenQueue:
        def put_nowait(self, *_):
            raise OSError("Simulated queue error")

    # ✅ Reset state before test
    NotificationManager._instance = None
    nm = NotificationManager()
    nm.reset()

    # 🔧 Inject a queue that always errors
    monkeypatch.setattr(nm, "_queue", BrokenQueue())

    # Should not raise, even though put_nowait() fails
    try:
        nm.notify("time.tick", 12345)
    except Exception:
        pytest.fail("NotificationManager should handle queue errors internally")
    finally:
        nm.stop()
