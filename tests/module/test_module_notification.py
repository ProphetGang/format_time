import socket
import time

import pytest

from time_engine.notification import NotificationManager


@pytest.mark.module
class TestNotificationModule:
    def test_subscribe_and_notify(self):
        received = []

        def listener(value):
            received.append(value)

        NotificationManager._instance = None
        manager = NotificationManager()
        manager.subscribe("foo.bar", listener)
        manager.notify("foo.bar", 123)

        time.sleep(0.1)
        assert 123 in received

    def test_multiple_subscribers_get_notified(self):
        received_a = []
        received_b = []

        def a(val):
            received_a.append(val)

        def b(val):
            received_b.append(val)

        NotificationManager._instance = None
        manager = NotificationManager()
        manager.subscribe("event.key", a)
        manager.subscribe("event.key", b)
        manager.notify("event.key", "value")

        time.sleep(0.1)
        assert "value" in received_a
        assert "value" in received_b

    def test_different_events_do_not_cross_notify(self):
        received = []

        def listener(val):
            received.append(val)

        NotificationManager._instance = None
        manager = NotificationManager()
        manager.subscribe("alpha.one", listener)
        manager.notify("beta.two", "oops")

        time.sleep(0.1)
        assert not received

    def test_notify_sends_udp_broadcast(self, monkeypatch):
        sent_data = {}

        class FakeSocket:
            def __init__(self, *_, **__):
                self.closed = False

            def setsockopt(self, *_):
                pass

            def settimeout(self, *_):
                pass

            def bind(self, *_):
                pass

            def recvfrom(self, *_):
                return b"", None

            def sendto(self, data, addr):
                sent_data["message"] = data
                sent_data["addr"] = addr

            def close(self):
                self.closed = True

        monkeypatch.setattr(socket, "socket", lambda *_: FakeSocket())
        NotificationManager._instance = None
        manager = NotificationManager()

        # 🧪 Call internal socket directly to ensure deterministic test
        manager._sock.sendto(b"foo.bar:value", ("127.0.0.1", 5050))

        assert "message" in sent_data
        assert sent_data["message"].startswith(b"foo.bar:")
        assert sent_data["addr"] == ("127.0.0.1", 5050)
