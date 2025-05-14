# flake8: noqa: E231
#!/usr/bin/env python
import argparse
import logging
import os

import numpy as np

from time_engine.api import MoonCycleAPI, SunCycleAPI
from time_engine.time import Time

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():
    parser = argparse.ArgumentParser(
        description="Advance time, generate calendars, or query sun/moon state."
    )
    parser.add_argument(
        "--ticks",
        type=int,
        default=0,
        help="Number of ticks to advance (default: 0)",
    )
    parser.add_argument(
        "--generate-sun-calendar",
        action="store_true",
        help="Generate and save sun_calendar.npy into time_engine/data/",
    )
    parser.add_argument(
        "--generate-moon-calendar",
        action="store_true",
        help="Generate and save moon_calendar.npy into time_engine/data/",
    )
    parser.add_argument(
        "--sun-altitude",
        nargs=2,
        metavar=("DAY", "TICK"),
        type=int,
        help="Lookup sun altitude for day (0-based) and tick",
    )
    parser.add_argument(
        "--sun-zenith",
        nargs=2,
        metavar=("DAY", "TICK"),
        type=int,
        help="Lookup sun zenith angle for day (0-based) and tick",
    )
    parser.add_argument(
        "--moon-altitude",
        nargs=2,
        metavar=("DAY", "TICK"),
        type=int,
        help="Lookup moon altitude for day (0-based) and tick",
    )
    parser.add_argument(
        "--moon-phase",
        type=int,
        metavar="DAY",
        help="Lookup moon phase fraction (0–1) for day (0-based)",
    )

    args = parser.parse_args()
    logger.debug("Parsed CLI args: %s", args)

    t = Time()

    # Set default calendar output path
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)
    sun_path = os.path.join(data_dir, "sun_calendar.npy")
    moon_path = os.path.join(data_dir, "moon_calendar.npy")

    if args.ticks:
        t.advance(args.ticks)
        dt = t.current_datetime()
        logger.info("Time advanced to: %s", dt)
        print(
            f"Year: {dt['year']}, Month: {dt['month']}, Day: {dt['day']}, "
            f"Hour: {dt['hour']}, Tick: {dt['tick']}"
        )

    if args.generate_sun_calendar:
        from time_engine.sun_calendar import SunCalendar

        logger.info("Generating sun calendar")
        SunCalendar(t).save(sun_path)
        print(f"Sun calendar written to {sun_path}")

    if args.generate_moon_calendar:
        from time_engine.moon_calendar import MoonCalendar

        logger.info("Generating moon calendar")
        MoonCalendar(t).save(moon_path)
        print(f"Moon calendar written to {moon_path}")

    if args.sun_altitude or args.sun_zenith:
        try:
            table = np.load(sun_path)
        except Exception as e:
            logger.error("Failed to load sun table: %s", e)
            return
        api = SunCycleAPI(table)
        day, tick = args.sun_altitude or args.sun_zenith
        logger.info("Querying SunCycleAPI: day=%d, tick=%d", day, tick)
        if args.sun_altitude:
            print(f"Sun altitude: {api.altitude(day, tick):.2f}°")
        if args.sun_zenith:
            print(f"Sun zenith: {api.zenith(day, tick):.2f}°")

    if args.moon_altitude or args.moon_phase is not None:
        try:
            table = np.load(moon_path)
        except Exception as e:
            logger.error("Failed to load moon table: %s", e)
            return
        api = MoonCycleAPI(table, lunar_cycle_days=t.months_per_year)
        logger.info("Querying MoonCycleAPI with lunar_cycle_days=%d", t.months_per_year)
        if args.moon_altitude:
            day, tick = args.moon_altitude
            print(f"Moon altitude: {api.altitude(day, tick):.2f}°")
        if args.moon_phase is not None:
            print(f"Moon phase: {api.phase(args.moon_phase):.2f}")


if __name__ == "__main__":
    main()
