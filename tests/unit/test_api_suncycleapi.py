import numpy as np
import pytest

from time_engine.api import SunCycleAPI


@pytest.mark.unit
class TestSunCycleAPI:
    def setup_method(self):
        self.table = np.array(
            [
                [10, 20, 30],
                [40, 50, 60],
                [70, 80, 90],
            ]
        )
        self.api = SunCycleAPI(self.table)

    def test_altitude_basic(self):
        result_1 = self.api.altitude(0, 1)
        result_2 = self.api.altitude(2, 2)
        assert result_1 == 20.0
        assert result_2 == 90.0

    def test_altitude_wraparound(self):
        result_1 = self.api.altitude(3, 0)  # wraps to day=0
        result_2 = self.api.altitude(1, 5)  # tick=5 % 3 = 2
        assert result_1 == 10.0
        assert result_2 == 60.0

    def test_zenith_complement(self):
        result_1 = self.api.zenith(0, 0)  # 90 - 10
        result_2 = self.api.zenith(2, 1)  # 90 - 80
        assert result_1 == 80.0
        assert result_2 == 10.0
