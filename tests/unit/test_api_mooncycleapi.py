import numpy as np
import pytest

from time_engine.api import MoonCycleAPI


@pytest.mark.unit
class TestMoonCycleAPI:
    def setup_method(self):
        self.table = np.array(
            [
                [1, 2],
                [3, 4],
                [5, 6],
                [7, 8],
            ]
        )
        self.api = MoonCycleAPI(self.table, lunar_cycle_days=4)

    def test_altitude_exact(self):
        result_1 = self.api.altitude(1, 1)
        result_2 = self.api.altitude(3, 0)
        assert result_1 == 4.0
        assert result_2 == 7.0

    def test_altitude_wraparound(self):
        result = self.api.altitude(4, 2)  # wraps to day=0, tick=0 → value = 1.0
        assert result == 1.0  # ✅ Fixed expected value

    @pytest.mark.parametrize(
        "day,tick,expected",
        [
            (0, 0, 0.0),
            (1, 0, 0.25),
            (2, 1, 0.625),  # (2 + 1/2) / 4 = 0.625
            (4, 2, 0.0),  # ✅ wraps to (0, 0)
        ],
    )
    def test_phase(self, day, tick, expected):
        actual = self.api.phase(day, tick)
        assert pytest.approx(actual, 0.01) == expected
