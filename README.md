<!-- Banner -->
<p align="center">
  <img src="assets/format_time.svg" alt="format_time Logo" width="300"/>
</p>

[![YouTube Subscribe](https://img.shields.io/badge/YouTube–Subscribe-red?style=social&logo=youtube)](https://youtube.com/format_life)

> A battle-tested, headless time & calendar engine for games, simulations, automation—and anything else that needs a clock.

---

## <img src="assets/caution_platform.svg" width="64" alt="Problem"/>  The Problem

Projects that simulate a world—whether it’s a game, a physics engine, a climate model, or an automation pipeline—inevitably need:

- **A reliable clock** with a reliable calendar to back it  
- **Accurate celestial data** (sunrise/sunset, moon phases, altitudes)  
- **Event hooks** so subsystems can react to time-changes  
- **Robust rollover logic** and edge-case handling  

> Rolling your own solution is **error-prone**, **time-consuming**, and quickly becomes a maintenance nightmare as your project grows.

---

## <img src="assets/lightbulb_platform.svg" width="64" alt="Solution"/>  My Solution: format_time

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
  - UDP-broadcast each time change  
  - Easy listeners for UIs, game loops, analytics pipelines  

- ✅ **Production-Quality**  
  - 112 tests (unit, edge-case, integration, module)  
  - Black / isort / flake8 pre-commit hooks  
  - Python 3.12+ support, MIT license  

---

## <img src="assets/box_platform.svg" width="64" alt="Installation"/>  Installation

__bash__  
- **Core engine only**  
  pip install format_time

- **GIS / astronomy extras** (sun & moon tables)  
  pip install format_time[geo]

- **Qt & matplotlib for custom UIs**  
  pip install format_time[ui]

- **Everything**  
  pip install format_time[geo,ui]

---

## 🎬 Quickstart

__python__  
1. **Initialize the engine**
   First, import and instantiate the unified module—this both sets up your clock and creates a local data        directory for the sun/moon tables.
   ```python 
   from time_engine.unified_time_module import UnifiedTimeModule  
   utm = UnifiedTimeModule(data_dir="calendar_data")`  
2. **Advance Time**
   Progress your simulation by “ticks.” Each tick is one unit of time; how many ticks make an hour is fully    configurable. Here, we jump ahead by 3,600 ticks:
   ```python
   utm.time.advance(3600)  
3. **Read the current datetime**
   Retrieve a human-readable breakdown of your simulation’s current time—year, month, day, hour, and tick:
   ```python
   dt = utm.time.current_datetime()
   print(
       `f"{dt['year']}-{dt['month']:02}-{dt['day']:02} 
   f"{dt['hour']:02}:{dt['tick']}/{utm.time.ticks_per_hour} ticks
   )  

4. **Query celestial data**
   Grab the sun’s altitude (or similarly the moon’s) based on your current date/time without any external API          calls:
   ```python
   sun_alt = utm.sun_api().get_altitude()
   print(f"Sun altitude: {sun_alt:.1f}°")  

5. **Listen for time-change events**
   If you need real-time updates in another process or UI, subscribe to UDP broadcasts emitted on each tick          advance. For example:
   ```python
   import socket
   sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   sock.bind(("0.0.0.0", 9999))
   data, _ = sock.recvfrom(1024)
   print("Time update:", data)

---

## 🔧 Configuration

`All core parameters live in a SQLite DB (default parameters.db). Change them on the fly:`
    
    
   from parameters.manager import ParametersManager  
   pm = ParametersManager()  
   pm.set("time", "hours_per_day", "30")  

   (calendars and notifications rebuild automatically)

---

Override the DB path

   export PARAM_DB_PATH=/path/to/my_params.db

---

## <img src="assets/collab_platform.svg" width="64" alt="Contributing"/>  Contributing

  
  **Fork & clone**  
  git clone git@github.com:YOUR_USERNAME/format_time.git  
  cd format_time

  **Install dev tools**  
  pip install -e .[dev]  
  pre-commit install  
  pre-commit run --all-files  
  pytest`

---

## 📄 License

This project is MIT-licensed. See [LICENSE](LICENSE) for details.

---

Build your world. Leave the clockwork to us.