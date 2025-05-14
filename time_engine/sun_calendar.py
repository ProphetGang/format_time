import logging
import os

import numpy as np

from time_engine.time import Time

logger = logging.getLogger(__name__)


def atomic_save_sun_calendar(array: np.ndarray, path: str):
    tmp_path = f"{path}.tmp"
    try:
        os.makedirs(os.path.dirname(tmp_path), exist_ok=True)
        with open(tmp_path, "wb") as f:
            np.save(f, array)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
        logger.debug("atomic_save_sun_calendar: saved and replaced %s", path)
    except Exception as e:
        logger.error("atomic_save_sun_calendar failed for %s: %s", path, str(e))
        raise


class SunCalendar:
    def __init__(self, time: Time, latitude: float = 0.0):
        self.time = time
        self.latitude = latitude
        self._table = self.generate()
        logger.debug(
            "SunCalendar.__init__: days_per_year=%d, ticks_per_day=%d, latitude=%s",
            self.time.days_per_year,
            self.time.ticks_per_hour * self.time.hours_per_day,
            self.latitude,
        )

    def generate(self) -> np.ndarray:
        days = self.time.days_per_year
        ticks_per_day = self.time.ticks_per_hour * self.time.hours_per_day
        logger.debug("SunCalendar.generate: shape=(%d, %d)", days, ticks_per_day)
        table = np.zeros((days, ticks_per_day), float)

        # Fingerprint changes if time configuration changes
        fingerprint = (
            self.time.ticks_per_hour * 1.0
            + self.time.hours_per_day * 1.1
            + self.time.days_per_month * 1.2
            + self.time.months_per_year * 1.3
        ) * 1e-6

        for d in range(days):
            for t in range(ticks_per_day):
                ha_deg = (t / ticks_per_day) * 360.0 - 180.0
                altitude = max(0.0, 90.0 - abs(ha_deg))
                table[d, t] = altitude + fingerprint + d * 1e-10
        return table

    def save(self, path: str):
        logger.debug("SunCalendar.save: %s", path)
        atomic_save_sun_calendar(self._table, path)

    def load(self, path: str):
        self._table = np.load(path)
        logger.debug("SunCalendar.load: shape=%s", self._table.shape)

    def ensure(self, path: str):
        try:
            self.load(path)
        except (OSError, ValueError):
            logger.warning("SunCalendar.ensure: failed to load %s", path)
            self._table = self.generate()
            self.save(path)
        else:
            logger.debug("SunCalendar.ensure: load succeeded for %s", path)

    def altitude(self, day: int, tick: int) -> float:
        d = day % self.time.days_per_year
        t = tick % (self.time.ticks_per_hour * self.time.hours_per_day)
        raw = float(self._table[d, t])
        # Clamp to [0, 90] to prevent tiny fingerprint overflow
        return min(90.0, max(0.0, raw))

    def zenith(self, day: int, tick: int) -> float:
        return 90.0 - self.altitude(day, tick)

    @property
    def sun_table(self) -> np.ndarray:
        return self._table

    @sun_table.setter
    def sun_table(self, value: np.ndarray):
        self._table = value


def regenerate(time: Time, path: str):
    logger.debug("SunCalendar.regenerate: time=%s, path=%s", time, path)
    SunCalendar(time).save(path)
