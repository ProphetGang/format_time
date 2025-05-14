import pytest

from time_engine.time import Time


@pytest.mark.unit
class TestTimeSetDatetime:
    def test_set_valid_datetime(self):
        t = Time(
            ticks_per_hour=10, hours_per_day=24, days_per_month=30, months_per_year=12
        )
        t.set_datetime(year=5, month=3, day=15, hour=12, tick=5)
        dt = t.current_datetime()
        breakpoint()  # Inspect after setting a valid datetime

        assert dt["year"] == 5
        assert dt["month"] == 3
        assert dt["day"] == 15
        assert dt["hour"] == 12
        assert dt["tick"] == 5

    def test_set_datetime_boundaries(self):
        t = Time(
            ticks_per_hour=4, hours_per_day=10, days_per_month=10, months_per_year=10
        )

        # Earliest time
        t.set_datetime(1, 1, 1, 0, 0)
        dt = t.current_datetime()
        breakpoint()  # Inspect edge case: min valid datetime
        assert dt == {"year": 1, "month": 1, "day": 1, "hour": 0, "tick": 0}

        # Latest time
        t.set_datetime(9999, 10, 10, 9, 3)
        dt = t.current_datetime()
        breakpoint()  # Inspect edge case: max valid datetime
        assert dt == {"year": 9999, "month": 10, "day": 10, "hour": 9, "tick": 3}

    @pytest.mark.parametrize(
        "field,value",
        [
            ("year", 0),
            ("month", 0),
            ("month", 13),
            ("day", 0),
            ("day", 31),
            ("hour", -1),
            ("hour", 24),
            ("tick", -1),
            ("tick", 10),
        ],
    )
    def test_invalid_set_datetime_values_raise(self, field, value):
        t = Time(
            ticks_per_hour=10, hours_per_day=24, days_per_month=30, months_per_year=12
        )
        kwargs = {"year": 1, "month": 1, "day": 1, "hour": 0, "tick": 0}
        kwargs[field] = value
        breakpoint()  # Observe kwargs just before triggering expected failure

        with pytest.raises(ValueError, match=f"Invalid {field}"):
            t.set_datetime(**kwargs)

    def test_set_datetime_overwrites_previous_state(self):
        t = Time()
        t.advance(1000)  # random advance
        breakpoint()  # Inspect state after advance before overwrite
        t.set_datetime(year=3, month=2, day=1, hour=0, tick=0)
        dt = t.current_datetime()
        breakpoint()  # Inspect final state to confirm overwrite

        assert dt["year"] == 3
        assert dt["month"] == 2
        assert dt["day"] == 1
        assert dt["hour"] == 0
        assert dt["tick"] == 0
