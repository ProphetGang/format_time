![format_time Logo](https://raw.githubusercontent.com/ProphetGang/format_time/raw/main/assets/format_time.svg)

[![YouTube Subscribe](https://img.shields.io/badge/YouTube–Subscribe-red?style=social&logo=youtube)](https://youtube.com/format_life)

> A battle-tested, headless time & calendar engine for games, simulations, automation—and anything else that needs a clock.

---

##  The Problem

![Problem Icon](https://raw.githubusercontent.com/ProphetGang/format_time/raw/main/assets/caution_platform.svg)

Projects that simulate a world—whether it’s a game, a physics engine, a climate model, or an automation pipeline—inevitably need:

- **A reliable clock** with a reliable calendar to back it  
- **Accurate celestial data** (sunrise/sunset, moon phases, altitudes)  
- **Event hooks** so subsystems can react to time-changes  
- **Robust rollover logic** and edge-case handling  

> Rolling your own solution is **error-prone**, **time-consuming**, and quickly becomes a maintenance nightmare as your project grows.

---

##  The Solution: format_time

![Solution Icon](https://raw.githubusercontent.com/ProphetGang/format_time/raw/main/assets/lightbulb_platform.svg)

**format_time** turns “build-an-engine-from-scratch” into “install-and-go.” It provides:

- 🎲 **Modular Core**  
  - Pure-Python `Time` class: `.advance(ticks)`, `.current_datetime()`  
  - Fully configurable calendar units (ticks/hr, hrs/day, days/month, months/yr)  

- 🌙 **Sun & Moon Tables**  
  - Precomputed NumPy arrays for fast altitude lookups  
  - Automatic rebuilds when you tweak calendar parameters  

- ♻️ **Dynamic Parameters**  
  - `ParametersManager` backed by SQLite  
  - Change any parameter at runtime—everything updates instantly  

- 🔔 **Event Notifications**  
  - UDP-broadcast on every tick advance  
  - Easy listeners for UIs, game loops, analytics pipelines  

- ✅ **Production-Quality**  
  - 112 tests (unit, edge-case, integration, module)  
  - Black / isort / flake8 pre-commit hooks  
  - Python 3.12+ support, MIT license  

---

##  Installation

![Installation Icon](https://raw.githubusercontent.com/ProphetGang/format_time/raw/main/assets/box_platform.svg)

```bash
# Core engine only
pip install format_time_engine

# GIS / astronomy extras (sun & moon tables)
pip install format_time_engine[geo]

# Qt & matplotlib for custom UIs
pip install format_time_engine[ui]

# Everything
pip install format_time_engine[geo,ui]
```

---

##  Quickstart ![Quickstart Icon](https://raw.githubusercontent.com/ProphetGang/format_time/raw/main/assets/quickstart_platform.svg)

```python
from time_engine.unified_time_module import UnifiedTimeModule
utm = UnifiedTimeModule(data_dir="calendar_data")

# Advance by 3,600 ticks
utm.time.advance(3600)

# Read current datetime
dt = utm.time.current_datetime()
print(
  f"{dt['year']}-{dt['month']:02}-{dt['day']:02} "
  f"{dt['hour']:02}:{dt['tick']}/{utm.time.ticks_per_hour} ticks"
)

# Query sun altitude
sun_alt = utm.sun_api().get_altitude()
print(f"Sun altitude: {sun_alt:.1f}°")
```

---

##  Configuration

![Configuration Icon](https://raw.githubusercontent.com/ProphetGang/format_time/raw/main/assets/configuration_platform.svg)

All core parameters live in a SQLite database (`parameters.db`). Change them on the fly:

```python
from parameters.manager import ParametersManager

pm = ParametersManager()
pm.set("time", "hours_per_day", "30")
# calendars and notifications rebuild automatically
```

Override the DB path:

```bash
export PARAM_DB_PATH=/path/to/my_params.db
```

---

##  Contributing

![Contributing Icon](https://raw.githubusercontent.com/ProphetGang/format_time/raw/main/assets/collab_platform.svg)

1. **Fork & clone**
   ```bash
   git clone git@github.com:ProphetGang/format_time.git
   cd format_time
   ```
2. **Install dev tools**
   ```bash
   pip install -e .[dev]
   pre-commit install
   pre-commit run --all-files
   pytest
   ```

---

##  License 

![License Icon](https://raw.githubusercontent.com/ProphetGang/format_time/raw/main/assets/license_platform.svg)

This project is MIT-licensed. See [LICENSE](LICENSE) for details.  