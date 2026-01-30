# AGENTS.md

Guidelines and improvement suggestions for AI agents working on this project.

## Project Overview

GPSModuleGT-U7 is a PyQt5-based GUI application for reading and displaying GPS data from the GT-U7 GPS module via serial connection. The codebase follows clean architecture principles with protocols, facades, and dependency injection.

## Code Style

- Python 3.7+ with type hints
- PyQt5 for GUI components
- Protocol-based interfaces in `protocols.py`
- Dependency injection for testability (see `serial_port.py`)

## Running Tests

```bash
source .venv/bin/activate
pytest tests/ -v
```

## Suggested Improvements

### High Priority

#### 1. Add `pyproject.toml`

Replace `requirements.txt` with modern Python packaging:

```toml
[project]
name = "gps-module-gt-u7"
version = "1.0.0"
description = "PyQt5 GPS module interface for GT-U7"
dependencies = [
    "PyQt5>=5.15.0",
    "pyserial>=3.5",
    "pynmea2>=1.18.0",
]

[project.optional-dependencies]
dev = ["pytest>=7.0.0", "mypy"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"

[tool.mypy]
python_version = "3.9"
ignore_missing_imports = true
```

#### 2. Enable Type Checking with mypy

The project has protocols defined but no type checking configured:

```bash
pip install mypy
mypy source/ --ignore-missing-imports
```

Fix any type errors discovered.

#### 3. Fix Import Inconsistency

In `source/nmea_parser.py:9`:

```python
# Current (incorrect)
from source.gps_data import GPSData

# Should be
from gps_data import GPSData
```

### Medium Priority

#### 4. Async GPS Polling

Currently `gps.py:80` uses blocking reads which can affect UI responsiveness:

```python
while self.ser.in_waiting() > 0:
    nmea_sentence = self._read_nmea_sentence()
```

Consider moving GPS polling to a `QThread`:

```python
class GPSReaderThread(QThread):
    data_received = pyqtSignal(GPSData)

    def run(self):
        while self._running:
            if self.ser.in_waiting() > 0:
                # read and emit signal
```

#### 5. Clean Up GPSControllerFacade

In `source/gps_controller_facade.py`:

- **Line 66**: Direct private attribute access breaks encapsulation:
  ```python
  # Current
  self._connection_manager._gps = gps_instance

  # Better: Add method to GPSConnectionManager
  def set_gps_instance(self, gps: GT_U7GPS) -> None:
      self._gps = gps
  ```

- **Line 176**: Empty method should be removed or implemented:
  ```python
  def set_update_callbacks(...) -> None:
      pass  # Remove this dead code
  ```

#### 6. Add pytest to requirements.txt

```
PyQt5>=5.15.0
pyserial>=3.5
pynmea2>=1.18.0
pytest>=7.0.0
```

### Low Priority

#### 7. Extract Utility Function

Move `format_variable_precision()` from `source/Panels/base_panel.py` to a dedicated utility module:

```
source/
  utils/
    __init__.py
    formatting.py  # format_variable_precision()
```

#### 8. Add Module Exports

In `source/actions/__init__.py`, define public API:

```python
from .export_action import ExportAction
from .refresh_action import RefreshAction
from .settings_action import SettingsAction

__all__ = ['ExportAction', 'RefreshAction', 'SettingsAction']
```

#### 9. Rename Reserved Word Parameter

In `source/Panels/base_panel.py:71`:

```python
# Current
def _set_value_safe(self, label, value, err, units, dir = ""):

# Better
def _set_value_safe(self, label: QLabel, value: float, err: float,
                    units: str, direction: str = "") -> None:
```

## Architecture Notes

- **Facade Pattern**: `GPSControllerFacade` provides unified interface to controllers
- **Protocol Interfaces**: `protocols.py` defines type-safe contracts
- **Factory Pattern**: `ApplicationFactory` handles app initialization
- **Dependency Injection**: `ISerialPort` allows mock serial for testing

## Testing

Tests use `MockSerialPort` from `tests/conftest.py` for hardware-independent testing. NMEA sentences in tests must have valid checksums (pynmea2 validates them).

Example valid sentence:
```
$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,47.0,M,,*4F
```
