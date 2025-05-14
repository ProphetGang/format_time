import logging
import os

import numpy as np

from time_engine.time import Time

logger = logging.getLogger(__name__)


def atomic_save_moon_calendar(array: np.ndarray, path: str):
    tmp_path = f"{path}.tmp"
    try:
        os.makedirs(os.path.dirname(tmp_path), exist_ok=True)
        with open(tmp_path, "wb") as f:
            np.save(f, array)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
        logger.debug("atomic_save_moon_calendar: saved and replaced %s", path)
    except Exception as e:
        logger.error("atomic_save_moon_calendar failed for %s: %s", path, str(e))
        raise


class MoonCalendar:
    def __init__(self, time: Time):
        self.time = time
        self.lunar_cycle_days = time.lunar_cycle_days
        self._table = self.generate()
        logger.debug(
            "MoonCalendar.__init__: days_per_year=%d, ticks_per_day=%d, lunar_cycle_days=%d",
            self.time.days_per_year,
            self.time.ticks_per_hour * self.time.hours_per_day,
            self.lunar_cycle_days,
        )

    def generate(self) -> np.ndarray:
        days = self.time.days_per_year
        ticks_per_day = self.time.ticks_per_hour * self.time.hours_per_day
        logger.debug("MoonCalendar.generate: shape=(%d, %d)", days, ticks_per_day)
        table = np.zeros((days, ticks_per_day), float)

        # Fingerprint derived from lunar_cycle_days only
        fingerprint = float(self.lunar_cycle_days) * 1.001e-6

        for d in range(days):
            phase = 2 * np.pi * (d % self.lunar_cycle_days) / self.lunar_cycle_days
            for t in range(ticks_per_day):
                ha = (t / ticks_per_day) * 2 * np.pi - np.pi
                table[d, t] = 50 * np.sin(phase + ha / 2) + fingerprint + d * 1e-10
        return table

    def save(self, path: str):
        logger.debug("MoonCalendar.save: %s", path)
        atomic_save_moon_calendar(self._table, path)

    def ensure(self, path: str):
        try:
            self._table = np.load(path)
        except (OSError, ValueError):
            logger.warning("MoonCalendar.ensure: failed to load %s", path)
            self._table = self.generate()
            self.save(path)
        else:
            logger.debug("MoonCalendar.ensure: load succeeded for %s", path)

    def altitude(self, day: int, tick: int) -> float:
        d = day % self.time.days_per_year
        t = tick % (self.time.ticks_per_hour * self.time.hours_per_day)
        return float(self._table[d, t])

    def phase_fraction(self, day: int) -> float:
        return float(day % self.lunar_cycle_days) / self.lunar_cycle_days

    def brightness(self, day: int) -> float:
        phase = (day % self.lunar_cycle_days) / self.lunar_cycle_days
        return float(np.clip(0.5 * (1 + np.cos(2 * np.pi * phase)), 0.0, 1.0))

    @property
    def moon_table(self) -> np.ndarray:
        return self._table

    @moon_table.setter
    def moon_table(self, value: np.ndarray):
        self._table = value


def regenerate(time: Time, path: str):
    logger.debug("MoonCalendar.regenerate: time=%s, path=%s", time, path)
    MoonCalendar(time).save(path)
