import pytest

from time_engine.time import Time


@pytest.mark.unit
class TestTimeCurrentDatetime:
    def test_initial_datetime_state(self):
        t = Time()
        dt = t.current_datetime()

        assert dt == {"year": 1, "month": 1, "day": 1, "hour": 0, "tick": 0}

    def test_after_tick_advance(self):
        t = Time(
            ticks_per_hour=2, hours_per_day=3, days_per_month=10, months_per_year=12
        )
        t.advance(5)  # 5 ticks → 2 ticks/hr = 2 full hrs + 1 tick

        dt = t.current_datetime()

        assert dt["year"] == 1
        assert dt["month"] == 1
        assert dt["day"] == 1
        assert dt["hour"] == 2
        assert dt["tick"] == 1

    def test_after_multiple_rollovers(self):
        t = Time(ticks_per_hour=1, hours_per_day=2, days_per_month=2, months_per_year=2)
        t.advance(20)  # should roll over all time units

        dt = t.current_datetime()

        assert dt == {
            "year": 3,
            "month": 2,  # ✅ Corrected: lands in month 2, not 1
            "day": 1,
            "hour": 0,
            "tick": 0,
        }

    def test_datetime_dict_structure(self):
        t = Time()
        dt = t.current_datetime()

        assert isinstance(dt, dict)
        for key in ["year", "month", "day", "hour", "tick"]:
            assert key in dt
            assert isinstance(dt[key], int)
