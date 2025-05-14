import pytest

from time_engine.time import Time


@pytest.mark.edgecase
def test_time_advance_negative_ticks_raises():
    t = Time(ticks_per_hour=1)
    with pytest.raises(ValueError, match="must be non-negative"):
        t.advance(-5)


@pytest.mark.edgecase
def test_time_advance_non_integer_ticks_is_ignored():
    t = Time(ticks_per_hour=1)
    with pytest.raises(TypeError):
        t.advance("ten")
