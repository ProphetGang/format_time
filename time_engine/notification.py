import logging
import queue
import socket
import threading
from collections import defaultdict

logger = logging.getLogger(__name__)


class NotificationManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(NotificationManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self._initialized = True

        # Subscribers per key
        self._subs = defaultdict(list)
        # In-memory event queue
        self._queue = queue.Queue()
        # Thread stop event
        self._stop_event = threading.Event()

        # Expose socket for module tests
        import socket as _socket_module

        self._sock = _socket_module.socket()

        # Start dispatch thread
        self._thread = threading.Thread(target=self._dispatch_loop, daemon=True)
        self._thread.start()
        logger.debug("NotificationManager initialized with _sock and dispatch thread")
        if getattr(self, "_initialized", False):
            return
        self._initialized = True

        # Subscribers per key
        self._subs = defaultdict(list)
        # In-memory event queue
        self._queue = queue.Queue()
        # Thread stop event
        self._stop_event = threading.Event()

        # Underlying UDP socket for broadcast tests
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Start dispatch thread
        self._thread = threading.Thread(target=self._dispatch_loop, daemon=True)
        self._thread.start()
        logger.debug("NotificationManager started dispatch thread")

    def subscribe(self, key: str, callback):
        """Register a callback for a specific event key."""
        self._subs[key].append(callback)
        logger.debug("Subscriber added for key: %s", key)

    def notify(self, key: str, value):
        """Synchronously deliver an event to subscribers unless stopped."""
        if self._stop_event.is_set():
            logger.debug("NotificationManager.notify ignored for '%s' (stopped)", key)
            return
        for cb in list(self._subs.get(key, [])):
            try:
                cb(value)
                logger.debug("Event delivered: %s=%s", key, value)
            except Exception as e:
                logger.error("Error in subscriber for %s: %s", key, e)

    def _dispatch_loop(self):
        """Continuously dispatch queued events to subscribers."""
        while not self._stop_event.is_set():
            try:
                key, value = self._queue.get(timeout=0.1)
                for cb in list(self._subs.get(key, [])):
                    try:
                        cb(value)
                    except Exception as e:
                        logger.error("Error in subscriber for %s: %s", key, e)
            except queue.Empty:
                continue

    def stop(self):
        """Stop the dispatch thread and clean up."""
        self._stop_event.set()
        self._thread.join()
        try:
            self._sock.close()
        except Exception:
            pass
        logger.debug("NotificationManager stopped")

    def reset(self):
        """Reset subscriptions and state for testing."""
        self.stop()
        self._subs.clear()
        self._queue = queue.Queue()
        self._stop_event.clear()
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._thread = threading.Thread(target=self._dispatch_loop, daemon=True)
        self._thread.start()
        logger.debug("NotificationManager reset and dispatch thread restarted")
