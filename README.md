# GPS Module GT-U7

A PyQt5-based GUI application for reading and displaying GPS data from the GT-U7 GPS module via serial connection. The
application displays real-time position data (latitude, longitude, altitude) and generates Meshtastic CLI commands for
easy integration.

## Features

- Real-time GPS position tracking with latitude, longitude, and altitude
- Satellite count and GPS fix quality display
- Automatic GPS reconnection on disconnect
- Interactive Settings dialog for serial port and configuration
- Adjustable GPS update intervals (50ms - 1000ms)
- Meshtastic CLI command generation with copy-to-clipboard
- Clean PyQt5 interface with multiple information panels
- GPS connection status monitoring with timestamps

## Requirements

- Python 3.7+
- PyQt5
- pyserial
- pynmea2

## Installation

1. Clone the repository:

```bash
git clone https://github.com/rnistuk/GPSModuleGT-U7.git
cd GPSModuleGT-U7
```

2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running from Command Line

```bash
python main.py
```

### Configuring GPS Settings

The application includes a built-in Settings dialog accessible via the "Settings" button in the GUI:

**Serial Port Configuration:**

- Auto-detect and select from available serial ports
- Manually enter custom port paths
- Adjust baud rate (4800 - 115200, default: 9600)

**Update Intervals:**

- GPS Update: 50ms - 1000ms (default: 100ms)
- Reconnection Interval: 1s - 30s (default: 5s)

**Alternative: Environment Variable**
You can still override the default port using an environment variable:

```bash
# macOS/Linux
GPS_PORT=/dev/ttyUSB0 python main.py

# Windows
set GPS_PORT=COM3
python main.py
```

### Running in PyCharm

1. Open the project in PyCharm
2. Ensure the virtual environment is configured (PyCharm should detect `.venv/`)
3. Right-click `main.py` and select "Run 'main'"
4. Use the Settings button in the GUI to configure GPS port and intervals

## Configuration

### Application Settings

All settings are configurable through the GUI Settings dialog:

- **Serial Port**: Select from detected ports or enter manually
- **Baud Rate**: Configure serial communication speed
- **GPS Update Interval**: How often to poll GPS data
- **Reconnection Interval**: Delay before attempting reconnection

Settings are applied immediately and persist for the current session.

### Panel Styling

Panel appearance can be customized in `Panels/panel_constants.py`:

- Panel dimensions, colors, borders
- Font sizes and label heights
- Common styling constants

### Logging

Logging is configured in `main.py`. To change log level, modify:

```python
logging.basicConfig(level=logging.DEBUG)  # For debug output
```

## GPS Module Connection

Ensure your GT-U7 GPS module is connected via USB serial adapter. The module should be configured for:

- Baud rate: 9600
- Data bits: 8
- Stop bits: 1
- Parity: None

## GUI Overview

The application features a clean, organized interface:

**Top Row:**

- **Position Panel**: Displays latitude, longitude, and height with units
- **Satellite Panel**: Shows satellite count and GPS fix quality

**Middle Row:**

- **GPS Status Panel**: Connection state and last update timestamp
- **Quick Actions Panel**: Refresh, Export Data, and Settings buttons

**Bottom:**

- **Meshtastic Command**: Auto-generated CLI command with Copy button

## Troubleshooting

**GPS not connecting:**

1. Click the "Settings" button and use "Scan Ports" to detect available ports
2. Check the serial port with `ls /dev/cu.*` (macOS) or `ls /dev/tty*` (Linux)
3. Ensure you have permission to access the serial port (may need `sudo` or add user to dialout group)
4. Verify the GPS module is properly connected and powered

**No GPS fix:**

- Ensure the GPS module has a clear view of the sky
- Wait 30-60 seconds for initial GPS lock
- Check satellite count and fix quality in the Satellite Panel
- GPS fix quality should show "GPS" or "DGPS" when locked

**Application crashes:**

- Check logs for error messages (logging configured in `main.py`)
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify PyQt5 is properly installed
- Try adjusting GPS update interval in Settings (increase if experiencing issues)

## License

MIT License

## Authors

**Richard Nistuk** - Initial development and hardware integration

### Acknowledgments

Code review, refactoring, and architecture improvements provided by Claude (Anthropic AI Assistant)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
