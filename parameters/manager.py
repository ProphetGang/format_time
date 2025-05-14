import threading
from collections import defaultdict

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from time_engine.notification import NotificationManager

Base = declarative_base()


class Parameter(Base):
    __tablename__ = "parameters"
    id = Column(Integer, primary_key=True)
    group = Column(String, index=True)
    key = Column(String, index=True)
    value = Column(String)


class ParametersManager:
    """
    SQLite-backed singleton parameter store with pub/sub notifications.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, db_url: str = "sqlite:///parameters.db", notifier=None):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            cls._instance._next_notifier = notifier
        return cls._instance

    def __init__(self, db_url: str = "sqlite:///parameters.db", notifier=None):
        # If already initialized, optionally inject or reset notifier
        if getattr(self, "_initialized", False):
            if notifier:
                self._notifier = notifier
            else:
                # Reset existing notifier only if it supports reset()
                if hasattr(self._notifier, "reset"):
                    self._notifier.reset()
            return

        # First-time setup: database engine and session
        self._engine = create_engine(db_url, future=True)
        Base.metadata.create_all(self._engine)
        self._Session = sessionmaker(bind=self._engine, future=True)

        # Initialize notifier (injected or singleton)
        self._notifier = (
            notifier or getattr(self, "_next_notifier", None) or NotificationManager()
        )
        self._initialized = True

    def get(self, group: str, key: str, default=None):
        """Retrieve a parameter value by group and key."""
        with self._Session() as session:
            p = session.query(Parameter).filter_by(group=group, key=key).one_or_none()
            return p.value if p else default

    def set(self, group: str, key: str, value):
        """Set a parameter and notify subscribers if the value changed."""
        notify_needed = False
        with self._Session() as session:
            p = session.query(Parameter).filter_by(group=group, key=key).one_or_none()
            if p is None:
                p = Parameter(group=group, key=key, value=str(value))
                session.add(p)
                notify_needed = True
            elif p.value != str(value):
                p.value = str(value)
                notify_needed = True
            session.commit()

        if notify_needed:
            event = f"{group}.{key}"
            self._notifier.notify(event, value)

    def on_change(self, group: str, key: str, callback):
        """Subscribe a callback to changes of a specific parameter."""
        event = f"{group}.{key}"
        self._notifier.subscribe(event, callback)

    def get_all(self):
        """Return all parameters grouped by their groups."""
        result = defaultdict(dict)
        with self._Session() as session:
            for p in session.query(Parameter).all():
                result[p.group][p.key] = p.value
        return dict(result)

    @classmethod
    def reset(cls):
        """Reset the singleton and stop the notifier for testing."""
        if cls._instance:
            try:
                cls._instance._notifier.stop()
            except Exception:
                pass
            cls._instance = None
