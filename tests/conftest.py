"""
Pytest fixtures for GPS Module tests.
"""
import sys
from pathlib import Path

import pytest

# Add source directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "source"))

from gps_data import GPSData
from serial_port import ISerialPort


class MockSerialPort(ISerialPort):
    """Mock serial port for testing without hardware."""

    def __init__(self, responses: list[bytes] = None):
        """
        Initialize mock serial port.

        Args:
            responses: List of byte responses to return from readline()
        """
        self._responses = responses or []
        self._index = 0
        self._is_open = True

    def add_response(self, response: str) -> None:
        """Add a response to the queue."""
        self._responses.append(response.encode('utf-8'))

    def readline(self) -> bytes:
        """Return next response from queue."""
        if self._index < len(self._responses):
            response = self._responses[self._index]
            self._index += 1
            return response
        return b''

    def is_open(self) -> bool:
        return self._is_open

    def close(self) -> None:
        self._is_open = False

    def in_waiting(self) -> int:
        """Return number of responses remaining."""
        return len(self._responses) - self._index


@pytest.fixture
def mock_serial():
    """Create a mock serial port."""
    return MockSerialPort()


@pytest.fixture
def gps_data():
    """Create a fresh GPSData instance."""
    return GPSData()


@pytest.fixture
def sample_gps_data():
    """Create GPSData with sample values."""
    return GPSData(
        latitude=49.2827,
        longitude=-123.1207,
        lat_dir='N',
        lon_dir='W',
        height=70.5,
        num_sats=8,
        gps_quality=1
    )


@pytest.fixture
def sample_nmea_gga():
    """Sample NMEA GGA sentence with position data."""
    return "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,47.0,M,,*47"


@pytest.fixture
def sample_nmea_rmc():
    """Sample NMEA RMC sentence."""
    return "$GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A"
