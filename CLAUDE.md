GPSModuleGT-U7 — CLAUDE.md
============================

A PyQt5 GUI for reading and displaying GPS data from the GT-U7 GPS module over a serial
connection. It shows real-time position (latitude, longitude, altitude), satellite
count and fix quality, and generates a Meshtastic CLI command for the current position.
The codebase is a deliberate exercise in clean architecture — protocols, facades,
factories, and dependency injection — so the hardware can be swapped for a mock and the
logic tested without a real GPS.

Project Structure
-----------------

Entry point is `source/main.py` (configures logging, builds the app via
`ApplicationFactory`, runs the Qt event loop). Run it from `source/`.

*   `source/gps.py` — `GT_U7GPS`: reads NMEA sentences from the serial port.
*   `source/serial_port.py` / `protocols.py` — `ISerialPort` protocol + real/mocked
    implementations; the dependency-injection seam that makes testing hardware-free.
*   `source/nmea_parser.py`, `gps_data.py` — parse NMEA into a `GPSData` value object
    (validated with `pynmea2`).
*   `source/gps_controller_facade.py`, `gps_connection_manager.py`,
    `gps_*_controller.py`, `view_update_coordinator.py`, `settings_mediator.py` —
    controller/facade layer coordinating reads, reconnection, and view updates.
*   `source/main_window.py`, `Panels/`, `settings_dialog.py`, `panel_factory.py`,
    `app_style.py` — the PyQt5 view (position / satellite / status panels, settings).
*   `source/actions/` — refresh / export / settings actions.
*   `source/command_formatter.py` — builds the Meshtastic CLI command.
*   `source/application_factory.py` — wires everything together at startup.
*   `tests/` — pytest suite; `conftest.py` provides `MockSerialPort`.

Architecture patterns in play: **Facade** (`GPSControllerFacade`), **Protocol
interfaces** (`protocols.py`), **Factory** (`ApplicationFactory`), **Dependency
injection** (`ISerialPort`).

Environment
-----------

*   IDE: PyCharm
*   Language: Python 3.7+ with type hints (mypy targets 3.9)
*   Build system: pip / `pyproject.toml` (project name `gps-module-gt-u7`)
*   Key dependencies: PyQt5 ≥ 5.15, pyserial ≥ 3.5, pynmea2 ≥ 1.18; dev: pytest ≥ 7,
    mypy. Tested on macOS/Linux against a GT-U7 over a USB serial adapter (9600 baud).

Building and Testing
--------------------

```
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"          # project + pytest + mypy
pytest tests/ -v                 # run tests
mypy source/ --ignore-missing-imports   # type check
```

Run the app:

```
cd source && python main.py
# or override the port: GPS_PORT=/dev/ttyUSB0 python main.py
```

Tests use `MockSerialPort` (from `tests/conftest.py`) so no hardware is needed. NMEA
sentences in tests must carry valid checksums — `pynmea2` validates them. Example:
`$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,47.0,M,,*4F`.

Conventions
-----------

*   TDD — write failing tests first, then minimum code to pass
*   No comments unless the why is non-obvious
*   No speculative code — only implement what is needed right now
*   Commit messages: short, descriptive, imperative tense ("add reconnection backoff" not "added" or "adding")
*   Python 3.7+ with type hints throughout; new interfaces go through Protocols in
    `protocols.py`
*   Inject dependencies (e.g. `ISerialPort`) rather than constructing hardware directly,
    so behaviour stays mockable
*   Keep view (`Panels/`, dialogs) thin; logic lives in the controller/facade layer

Current State
-------------

### Completed

*   Real-time position, satellite count, and fix-quality display in a PyQt5 GUI
*   Serial reading via `GT_U7GPS` with automatic reconnection on disconnect
*   Settings dialog (serial port scan/select, baud rate, update + reconnection intervals)
*   Meshtastic CLI command generation with copy-to-clipboard
*   Clean-architecture layering (facade, protocols, factory, DI) with a pytest suite over
    NMEA parsing, GPS reads, command formatting, and `GPSData`

### In Progress

*   Nothing in flight

### Next

*   Run mypy clean and fix reported type errors (config already in `pyproject.toml`)
*   Fix import inconsistency in `source/nmea_parser.py` (`from source.gps_data` →
    `from gps_data`)
*   Move blocking GPS polling (`gps.py`) onto a `QThread` so the UI stays responsive
*   Tidy `GPSControllerFacade` — remove direct private-attribute access and dead
    `set_update_callbacks` no-op; declare `__all__` in `actions/__init__.py`; extract
    `format_variable_precision` into a `utils/` module

### Decisions Pending

*   None

Do Not Touch
------------

*   Nothing off limits at this time.

Pair Programming
----------------

*   Driver writes all code — navigator (Claude) does not write code unless explicitly asked
*   Navigator provides: direction, design decisions, code review, and course corrections
*   One step at a time — navigator waits for driver to confirm before moving to the next
*   Navigator confirms tests pass before suggesting the next step
*   Navigation is terse — no lengthy explanations unless explicitly asked
*   If navigator disagrees with an approach, say so once then follow the driver's lead

Karpathy Rules
--------------

All rules apply to every task unless explicitly overridden.

### Rule 1 — Think Before Coding

State assumptions explicitly. If uncertain, ask rather than guess. Present multiple interpretations when ambiguity exists. Push back when a simpler approach exists. Stop when confused. Name what's unclear.

### Rule 2 — Simplicity First

Minimum code that solves the problem. Nothing speculative. No features beyond what was asked. No abstractions for single-use code. Test: would a senior engineer say this is overcomplicated? If yes, simplify.

### Rule 3 — Surgical Changes

The driver should touch only what is necessary to make the current test pass. Don't "improve" adjacent code, comments, or formatting. Don't refactor what isn't broken. Match existing style. Navigator warns the driver if this rule is being broken.

### Rule 4 — Agree on Done Before Starting

Before implementing anything, both driver and navigator should agree on what done looks like. A failing test is the preferred success criterion. Don't start until done is defined.

### Rule 5 — Dropped

Original rule was written for agentic coding and does not apply to this pair programming model.

### Rule 6 — Know When to Stop

If the session is getting long or context feels stale, checkpoint before continuing. Summarise what's done, what's verified, what's next. Update CLAUDE.md to reflect current state, then commit before ending the session. A fresh session with good context beats a stale one with accumulated confusion.

### Rule 7 — Surface Conflicts, Don't Average Them

If two patterns contradict, pick one (more recent / more tested). Explain why. Flag the other for cleanup. Don't blend conflicting patterns.

### Rule 8 — Read Before You Write

Before adding code, read exports, immediate callers, shared utilities. "Looks orthogonal" is dangerous. If unsure why code is structured a way, ask.

### Rule 9 — Test Behaviours, Not Functionality

Tests verify what the code does from the outside, not how it does it internally. Tests must encode WHY the behaviour matters, not just WHAT it does. A test that can't fail when business logic changes is wrong.

### Rule 10 — Checkpoint After Every Significant Step

Summarize what was done, what's verified, what's left. Don't continue from a state you can't describe back. If you lose track, stop and restate.

### Rule 11 — Match the Codebase's Conventions, Even If You Disagree

Conformance > taste inside the codebase. If you genuinely think a convention is harmful, surface it. Don't fork silently.

### Rule 12 — Fail Loud

"Completed" is wrong if anything was skipped silently. "Tests pass" is wrong if any were skipped. Default to surfacing uncertainty, not hiding it.
