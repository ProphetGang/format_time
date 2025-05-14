import pytest

from time_engine.moon_calendar import MoonCalendar
from time_engine.sun_calendar import SunCalendar
from time_engine.time import Time


@pytest.mark.edgecase
def test_sun_calendar_handles_corrupted_file(tmp_path):
    """Ensure SunCalendar regenerates safely when a .npy file is corrupted."""
    time_cfg = Time()
    calendar_path = tmp_path / "calendar"
    calendar_path.mkdir()

    # Simulate corrupted file
    corrupted = calendar_path / "sun_table.npy"
    with open(corrupted, "wb") as f:
        f.write(b"This is not a valid numpy file")

    calendar = SunCalendar(time_cfg)
    calendar.ensure(str(corrupted))
    assert calendar.sun_table.shape[0] == time_cfg.days_per_year


@pytest.mark.edgecase
def test_moon_calendar_handles_corrupted_file(tmp_path):
    """Ensure MoonCalendar regenerates safely when a .npy file is corrupted."""
    time_cfg = Time()
    calendar_path = tmp_path / "calendar"
    calendar_path.mkdir()

    # Corrupt the moon table
    corrupted = calendar_path / "moon_table.npy"
    with open(corrupted, "wb") as f:
        f.write(b"Not valid binary format")

    calendar = MoonCalendar(time_cfg)
    calendar.ensure(str(corrupted))
    assert calendar.moon_table.shape[0] == time_cfg.days_per_year
