![format_time Logo](https://github.com/ProphetGang/format_time/raw/main/assets/format_time.svg)

[![YouTube Subscribe](https://img.shields.io/badge/YouTube–Subscribe-red?style=social&logo=youtube)](https://youtube.com/format_life)

> A battle-tested, headless time & calendar engine for games, simulations, automation—and anything else that needs a clock.

---

##  Problem&nbsp;
<img
  src="https://github.com/ProphetGang/format_time/raw/main/assets/caution_platform.svg"
  alt="Problem Icon"
  width="64"
  height="64"
  style="vertical-align:middle"
/>

Projects that simulate a world—whether it’s a game, a physics engine, a climate model, or an automation pipeline—inevitably need:

- **A reliable clock** with a reliable calendar to back it  
- **Accurate celestial data** (sunrise/sunset, moon phases, altitudes)  
- **Event hooks** so subsystems can react to time-changes  
- **Robust rollover logic** and edge-case handling  

> Rolling your own solution is **error-prone**, **time-consuming**, and quickly becomes a maintenance nightmare as your project grows.

---

##  Solution&nbsp;
<img
  src="https://github.com/ProphetGang/format_time/raw/main/assets/lightbulb_platform.svg"
  alt="Solution Icon"
  width="64"
  height="64"
  style="vertical-align:middle"
/>

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

##  Installation&nbsp;
<img
  src="https://github.com/ProphetGang/format_time/raw/main/assets/box_platform.svg"
  alt="Installation Icon"
  width="64"
  height="64"
  style="vertical-align:middle"
/>

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

##  Quickstart&nbsp;
<img
  src="https://github.com/ProphetGang/format_time/raw/main/assets/quickstart_platform.svg"
  alt="Quickstart Icon"
  width="64"
  height="64"
  style="vertical-align:middle"
/>

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

##  Configuration&nbsp;
<img
  src="https://github.com/ProphetGang/format_time/raw/main/assets/configuration_platform.svg"
  alt="Configuration Icon"
  width="64"
  height="64"
  style="vertical-align:middle"
/>

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

##  Contributing&nbsp;
<img
  src="https://github.com/ProphetGang/format_time/raw/main/assets/collab_platform.svg"
  alt="Contributing Icon"
  width="64"
  height="64"
  style="vertical-align:middle"
/>

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

##  License&nbsp;
<img
  src="https://github.com/ProphetGang/format_time/raw/main/assets/license_platform.svg"
  alt="License Icon"
  width="64"
  height="64"
  style="vertical-align:middle"
/>

This project is MIT-licensed. See [LICENSE](LICENSE) for details.  