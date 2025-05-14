import logging
import os
from collections import defaultdict

import numpy as np

from parameters.manager import ParametersManager
from time_engine.api import MoonCycleAPI, SunCycleAPI
from time_engine.moon_calendar import MoonCalendar
from time_engine.sun_calendar import SunCalendar
from time_engine.time import Time

logger = logging.getLogger(__name__)


class UnifiedTimeModule:
    def __init__(self, data_dir: str = None, params: ParametersManager = None):
        # Prepare data directory
        base = data_dir or os.path.join(os.path.dirname(__file__), "data")
        os.makedirs(base, exist_ok=True)
        self.sun_path = os.path.join(base, "sun_calendar.npy")
        self.moon_path = os.path.join(base, "moon_calendar.npy")
        logger.debug(
            "UnifiedTimeModule data paths: sun=%s, moon=%s",
            self.sun_path,
            self.moon_path,
        )

        # Parameter manager (injected or singleton)
        self.pm = params or ParametersManager()
        # If no external notifier was provided at construction, use in-process notifier
        injected = getattr(self.pm, "_next_notifier", None)
        if injected is None:

            class SimpleNotifier:
                def __init__(self):
                    self._subs = defaultdict(list)

                def subscribe(self, event, callback):
                    self._subs[event].append(callback)

                def notify(self, event, value):
                    for cb in list(self._subs.get(event, [])):
                        cb(value)

                def stop(self):
                    pass

            self.pm._notifier = SimpleNotifier()
        # Only override notifier if none was injected
        if params is None:

            class SimpleNotifier:
                def __init__(self):
                    self._subs = defaultdict(list)

                def subscribe(self, event, callback):
                    self._subs[event].append(callback)

                def notify(self, event, value):
                    for cb in list(self._subs.get(event, [])):
                        cb(value)

                def stop(self):
                    pass

            self.pm._notifier = SimpleNotifier()

        # Initialize time and dirty flags
        self.time = Time()
        self._calendar_dirty_flags = {"sun": False, "moon": False}
        self._initialized = False

        # Register change listeners
        keys = ("ticks_per_hour", "hours_per_day", "days_per_month", "months_per_year")
        for key in keys:
            self.pm.on_change(
                "time", key, lambda v, k=key: self._on_param_change(k, int(v))
            )
        self.pm.on_change(
            "time",
            "lunar_cycle_days",
            lambda v: self._on_param_change("lunar_cycle_days", int(v)),
        )
        logger.debug("UnifiedTimeModule registered on_change callbacks")

        # Load or initialize parameter values into self.time
        for key in keys:
            val = self.pm.get("time", key)
            if val is None:
                default = getattr(self.time, key)
                self.pm.set("time", key, str(default))
                val = default
            setattr(self.time, key, int(val))
        lcd_val = self.pm.get("time", "lunar_cycle_days")
        if lcd_val is None:
            self.pm.set("time", "lunar_cycle_days", str(self.time.lunar_cycle_days))
        else:
            self.time.lunar_cycle_days = int(lcd_val)
        logger.debug(
            "UnifiedTimeModule applied parameter values to Time: %s", self.time
        )

        # Ensure initial calendars exist
        self._ensure_calendars()

        # Load saved tables and APIs
        self.sun_table = np.load(self.sun_path)
        raw_moon = np.load(self.moon_path)
        if raw_moon.ndim == 1:
            raw_moon = raw_moon.reshape(-1, 1)
        self.moon_table = raw_moon

        lcd = self.time.lunar_cycle_days
        self.sun_api = SunCycleAPI(self.sun_table)
        self.moon_api = MoonCycleAPI(self.moon_table, lunar_cycle_days=lcd)
        logger.debug("UnifiedTimeModule initialized APIs")

        self._initialized = True

    def _on_param_change(self, key: str, value: int):
        setattr(self.time, key, value)
        if not self._initialized:
            return

        if key in {"days_per_month", "months_per_year"}:
            self._calendar_dirty_flags["sun"] = True
            self._calendar_dirty_flags["moon"] = True
        elif key in {"ticks_per_hour", "hours_per_day"}:
            self._calendar_dirty_flags["sun"] = True
        elif key == "lunar_cycle_days":
            self._calendar_dirty_flags["moon"] = True

        self.rebuild_calendars()

    def rebuild_calendars(self):
        # Rebuild Time from params
        new_time = Time()
        keys = ("ticks_per_hour", "hours_per_day", "days_per_month", "months_per_year")
        for key in keys:
            val = self.pm.get("time", key)
            setattr(new_time, key, int(val))
        lcd_val = self.pm.get("time", "lunar_cycle_days")
        new_time.lunar_cycle_days = int(lcd_val)
        new_time.days_per_year = new_time.days_per_month * new_time.months_per_year
        self.time = new_time

        # Regenerate flagged calendars
        if self._calendar_dirty_flags["sun"]:
            SunCalendar(self.time).save(self.sun_path)
        if self._calendar_dirty_flags["moon"]:
            MoonCalendar(self.time).save(self.moon_path)

        # Reload tables and APIs
        self.sun_table = np.load(self.sun_path)
        raw_moon = np.load(self.moon_path)
        if raw_moon.ndim == 1:
            raw_moon = raw_moon.reshape(-1, 1)
        self.moon_table = raw_moon

        lcd = self.time.lunar_cycle_days
        self.sun_api = SunCycleAPI(self.sun_table)
        self.moon_api = MoonCycleAPI(self.moon_table, lunar_cycle_days=lcd)

        # Clear flags
        self._calendar_dirty_flags = {"sun": False, "moon": False}

    def _ensure_calendars(self):
        os.makedirs(os.path.dirname(self.sun_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.moon_path), exist_ok=True)
        if not os.path.exists(self.sun_path):
            SunCalendar(self.time).save(self.sun_path)
        if not os.path.exists(self.moon_path):
            MoonCalendar(self.time).save(self.moon_path)
