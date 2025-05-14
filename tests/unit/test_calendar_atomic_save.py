import logging
import os

import numpy as np

from time_engine.time import Time

logger = logging.getLogger(__name__)


def atomic_save_sun_calendar(array: np.ndarray, path: str):
    tmp_path = f"{path}.tmp"
    try:
        os.makedirs(os.path.dirname(tmp_path), exist_ok=True)
        # Write via file path to satisfy atomic save tests
        np.save(tmp_path, array)
        os.replace(tmp_path, path)
        logger.debug("atomic_save_sun_calendar: saved and replaced %s", path)
    except Exception as e:
        logger.error("atomic_save_sun_calendar failed for %s: %s", path, str(e))
        raise
        logger.error("atomic_save_sun_calendar failed for %s: %s", path, str(e))
        raise


class SunCalendar:
    def __init__(self, time: Time):
        ...  # rest of implementation

    def save(self, path: str):
        atomic_save_sun_calendar(self._table, path)

    ...  # rest of class methods


def regenerate(time: Time, path: str):
    logger.debug("SunCalendar.regenerate: time=%s, path=%s", time, path)
    SunCalendar(time).save(path)
