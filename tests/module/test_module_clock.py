import sys

import numpy as np
import pytest

from time_engine import clock


@pytest.mark.module
class TestClockModule:
    def test_clock_demo_prints_day_cycle(self, monkeypatch, capsys):
        monkeypatch.setattr(sys, "argv", ["clock.py", "--ticks", "48"])
        clock.main()
        captured = capsys.readouterr()
        assert "Year:" in captured.out
        assert "Tick:" in captured.out

    def test_advance_outputs_expected_ticks_and_rollover(self, monkeypatch, capsys):
        monkeypatch.setattr(sys, "argv", ["clock.py", "--ticks", "120"])
        clock.main()
        captured = capsys.readouterr()
        assert "Hour:" in captured.out
        assert "Tick:" in captured.out

    def test_clock_handles_multiple_rollovers(self, monkeypatch, capsys):
        monkeypatch.setattr(sys, "argv", ["clock.py", "--ticks", "1000"])
        clock.main()
        captured = capsys.readouterr()
        assert "Year:" in captured.out
        assert "Day:" in captured.out
