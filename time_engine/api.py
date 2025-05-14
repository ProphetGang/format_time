import logging

import numpy as np

logger = logging.getLogger(__name__)


class SunCycleAPI:
    """
    Runtime lookup for sun altitude & zenith given a day index and tick index.
    """

    def __init__(self, sun_table: np.ndarray):
        """
        Args:
            sun_table (np.ndarray): 2D array of shape (days_per_year, ticks_per_day)
                                    containing sun altitudes.
        """
        self.sun_table = sun_table
        self.days_per_year, self.ticks_per_day = sun_table.shape
        logger.debug(
            "SunCycleAPI.__init__: shape=(%d, %d)",
            self.days_per_year,
            self.ticks_per_day,
        )

    def altitude(self, day: int, tick: int) -> float:
        """
        Returns the sun's altitude for a given day and tick, wrapping if out of bounds.

        Args:
            day (int): Day index (wraps over days_per_year).
            tick (int): Tick index (wraps over ticks_per_day).

        Returns:
            float: Altitude in degrees.
        """
        d = day % self.days_per_year
        t = tick % self.ticks_per_day
        logger.debug("SunCycleAPI.altitude: day=%d→%d, tick=%d→%d", day, d, tick, t)
        return float(self.sun_table[d, t])

    def zenith(self, day: int, tick: int) -> float:
        """
        Returns the sun's zenith angle, which is 90° minus altitude.

        Args:
            day (int): Day index.
            tick (int): Tick index.

        Returns:
            float: Zenith angle in degrees.
        """
        alt = self.altitude(day, tick)
        logger.debug("SunCycleAPI.zenith: altitude=%f → zenith=%f", alt, 90.0 - alt)
        return 90.0 - alt

    def __repr__(self):
        return f"<SunCycleAPI shape=({self.days_per_year}, {self.ticks_per_day})>"


class MoonCycleAPI:
    """
    Runtime lookup for moon altitude & phase given a day index and tick index.
    """

    def __init__(self, moon_table: np.ndarray, lunar_cycle_days: int):
        """
        Args:
            moon_table (np.ndarray): 2D array of shape (days_per_year, ticks_per_day)
                                     containing moon altitudes.
            lunar_cycle_days (int): Length of the full lunar cycle in days.
        """
        self.moon_table = moon_table
        self.days_per_year, self.ticks_per_day = moon_table.shape
        self.lunar_cycle_days = lunar_cycle_days
        logger.debug(
            "MoonCycleAPI.__init__: days_per_year=%d, ticks_per_day=%d, lunar_cycle_days=%d",
            self.days_per_year,
            self.ticks_per_day,
            self.lunar_cycle_days,
        )

    def altitude(self, day: int, tick: int) -> float:
        """
        Returns the moon's altitude, wrapping over bounds as needed.

        Args:
            day (int): Day index (wraps over days_per_year).
            tick (int): Tick index (wraps over ticks_per_day).

        Returns:
            float: Moon altitude in degrees.
        """
        d = day % self.days_per_year
        t = tick % self.ticks_per_day
        logger.debug("MoonCycleAPI.altitude: day=%d→%d, tick=%d→%d", day, d, tick, t)
        return float(self.moon_table[d, t])

    def phase(self, day: int, tick: int = 0) -> float:
        """
        Returns the normalized moon phase [0.0, 1.0), with optional tick precision.

        Args:
            day (int): Day index.
            tick (int): Optional tick index for fractional phase resolution.

        Returns:
            float: Fraction of lunar cycle elapsed (0.0 = new moon, 0.5 = full moon).
        """
        day_cycle = (day % self.lunar_cycle_days) + (
            tick % self.ticks_per_day
        ) / self.ticks_per_day
        phase_frac = (day_cycle % self.lunar_cycle_days) / self.lunar_cycle_days
        logger.debug(
            "MoonCycleAPI.phase: day_cycle=%f → phase_frac=%f", day_cycle, phase_frac
        )
        return phase_frac

    def zenith(self, day: int, tick: int) -> float:
        """
        Returns the moon's zenith angle, which is 90° minus altitude.

        Args:
            day (int): Day index.
            tick (int): Tick index.

        Returns:
            float: Zenith angle in degrees.
        """
        alt = self.altitude(day, tick)
        logger.debug("MoonCycleAPI.zenith: altitude=%f → zenith=%f", alt, 90.0 - alt)
        return 90.0 - alt

    def __repr__(self):
        return (
            f"<MoonCycleAPI shape=({self.days_per_year}, {self.ticks_per_day}), "
            f"lunar_cycle_days={self.lunar_cycle_days}>"
        )
