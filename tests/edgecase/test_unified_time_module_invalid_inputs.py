import pytest

from time_engine.unified_time_module import UnifiedTimeModule


@pytest.mark.edgecase
def test_unified_time_module_rejects_negative_calendar_config(tmp_path):
    """
    Validates that UnifiedTimeModule raises an error or behaves safely
    when given invalid time configurations (e.g. negative values).
    """
    data_dir = tmp_path / "bad_data"

    # Patch in a broken config class manually if needed
    from time_engine.time import Time

    class BadTime(Time):
        def __init__(self):
            super().__init__(
                ticks_per_hour=-1,  # invalid
                hours_per_day=24,
                days_per_month=30,
                months_per_year=12,
            )

    # Create UnifiedTimeModule
    utm = UnifiedTimeModule(data_dir=str(data_dir))

    # Inject bad time instance manually (should raise at creation)
    with pytest.raises(ValueError, match="ticks_per_hour must be positive"):
        utm.time = BadTime()
