# 🧪 Test Suite Overview — `planet_sim`

This document describes the test architecture, naming conventions, and workflow for verifying and validating the simulation engine.

---

## 📁 Test Directory Structure

All tests are located in the `tests/` folder, structured by purpose:

tests/
├── module/ # A: Module-level black-box tests
├── unit/ # B: Individual function/method tests
├── integration/ # C: Inter-module interaction tests
├── edge_cases/ # E: Boundary conditions and defensive assertions
└── conftest.py # Shared fixtures for test isolation and mocking

---

## 🏷️ Naming Conventions

### 🗂 File Naming

| Test Type     | Filename Pattern                                 | Example                                 |
|---------------|--------------------------------------------------|-----------------------------------------|
| Module        | `test_module_<module_name>.py`                   | `test_module_time.py`                   |
| Unit          | `test_<module>_<function_or_behavior>.py`        | `test_time_advance.py`                  |
| Integration   | `test_<modA>_<funcA>_to_<modB>_<funcB>.py`       | `test_time_to_api_query_consistency.py` |
| Edge Case     | `test_<module>_<edge_case_description>.py`       | `test_unified_time_module_invalid.py`   |

---

### 🧪 Test Class & Function Structure

```python
# Module test (A)
@pytest.mark.module
class TestTimeModule:
    def test_advance_over_a_year(self): ...

# Unit test (B)
@pytest.mark.unit
def test_time_advance(): ...

# Integration test (C)
@pytest.mark.integration
def test_time_to_api_query_consistency(): ...

# Edge case (D)
@pytest.mark.edge
def test_manager_on_null_path(): ...

🧰 Fixtures & Mocking
Shared in tests/conftest.py:

✅ Isolated database state via in-memory SQLite

✅ Synthetic calendars for moon/sun

✅ Monkeypatch utilities

✅ Temp paths for file-safe generation

##Running the Tests

Basic execution:

pytest

To run by category:

pytest -m unit
pytest -m module
pytest -m integration
pytest -m edge

📈 Coverage & CI
Use pytest-cov to enforce thresholds:

pytest --cov=time_engine --cov-report=term-missing

🧪 Guidelines for Writing New Tests

Rule  	                                                     Description
❗ Each new module must have module + unit tests	             Add both A and B tests with meaningful naming
🔗 Any module interaction must be covered in C tests	     E.g. unified time pushing into API, parameters into calendars
⚠️ Edge case for every user-modifiable input or config	     Nulls, invalid values, overflow risk, corrupted files, etc
✅ Use caplog, monkeypatch, and temp paths for robustness    Avoid file locks or dirty state

By following this guide, planet_sim’s test suite remains clean, discoverable, and fully aligned with real-world changes. Developers can safely refactor or extend without fear of silent breakages.


