# tests/module/test_module_api.py

import numpy as np
import pytest

from time_engine.api import MoonCycleAPI, SunCycleAPI


@pytest.mark.module
class TestApiModule:
    def test_sun_cycle_altitude_and_zenith_query(self):
        table = np.array(
            [
                [0.0, 15.0, 30.0],
                [10.0, 25.0, 40.0],
                [20.0, 35.0, 50.0],
                [30.0, 45.0, 60.0],
            ]
        )
        api = SunCycleAPI(table)

        assert api.altitude(1, 0) == 10.0
        assert api.altitude(2, 1) == 35.0
        assert api.altitude(3, 2) == 60.0

        assert api.zenith(1, 0) == 80.0
        assert api.zenith(2, 1) == 55.0
        assert api.zenith(3, 2) == 30.0

    def test_moon_cycle_phase_and_altitude_query(self):
        table = np.array(
            [
                [5.0, 10.0, 15.0],  # day 0
                [20.0, 25.0, 30.0],  # day 1
                [35.0, 40.0, 45.0],  # day 2
                [50.0, 55.0, 60.0],  # day 3
            ]
        )
        lunar_cycle_days = 4
        api = MoonCycleAPI(table, lunar_cycle_days=lunar_cycle_days)

        assert api.phase(1, 0) == pytest.approx(0.25, 0.01)
        assert api.phase(2, 1) == pytest.approx(0.5833, 0.01)
        assert api.phase(4, 2) == pytest.approx(0.1667, 0.01)

        assert api.altitude(1, 0) == 20.0
        assert api.altitude(2, 1) == 40.0
        assert api.altitude(4, 2) == 15.0
        assert api.altitude(5, 0) == 20.0

        assert api.zenith(1, 0) == 70.0
        assert api.zenith(2, 1) == 50.0
        assert api.zenith(4, 2) == 75.0
        assert api.zenith(5, 0) == 70.0

    def test_wraparound_indices(self):
        table = np.array(
            [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9],
            ]
        )
        api = SunCycleAPI(table)

        # Day 4 % 3 = 1, Tick 5 % 3 = 2
        assert api.altitude(4, 5) == 6
        assert api.zenith(4, 5) == 84.0
