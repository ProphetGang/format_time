# tests/unit/test_manager_on_change.py

import pytest

from parameters.manager import ParametersManager


@pytest.mark.unit
def test_manager_on_change():
    local_notifications = []

    pm = ParametersManager()

    # Register the callback to be triggered when 'temperature' changes
    pm.on_change(
        "climate", "temperature", lambda v: local_notifications.append(("temp", v))
    )

    # Set the new value, which should trigger the callback
    pm.set("climate", "temperature", 30)

    # Debugging: Print the list of notifications to see if the callback was invoked
    print("Notifications:", local_notifications)

    # Assert that the callback was triggered with the correct value
    assert (
        "temp",
        30,
    ) in local_notifications  # Ensure the value was correctly appended to the list
