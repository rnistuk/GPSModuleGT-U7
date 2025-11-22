"""
Serial port interface and implementation for GPS communication.
Provides abstraction over serial communication to enable testing and flexibility.
"""
import logging
from abc import ABC, abstractmethod

import serial

logger = logging.getLogger(__name__)


class ISerialPort(ABC):
    """Interface for serial port communication."""

    @abstractmethod
    def readline(self) -> bytes:
        """Read a line from the serial port."""
        pass

    @abstractmethod
    def is_open(self) -> bool:
        """Check if the serial port is open."""
        pass

    @abstractmethod
    def close(self):
        """Close the serial port."""
        pass

    @abstractmethod
    def in_waiting(self) -> int:
        """Get the number of bytes waiting to be read."""
        pass


class SerialPort(ISerialPort):
    """Concrete implementation of serial port using pyserial."""

    def __init__(self, port: str, baudrate: int = 9600, timeout: float = 1):
        """
        Initialize serial port connection.

        Args:
            port: Serial port device path (e.g., '/dev/cu.usbmodem2101')
            baudrate: Communication speed (default: 9600)
            timeout: Read timeout in seconds (default: 1)

        Raises:
            RuntimeError: If serial port cannot be opened
        """
        try:
            self._serial = serial.Serial(port, baudrate, timeout=timeout)
            logger.info(f"Serial port {port} opened successfully at {baudrate} baud")
        except serial.SerialException as e:
            logger.error(f"Error opening serial port {port}: {e}")
            raise RuntimeError(f"Failed to open serial port {port}: {e}")

    def readline(self) -> bytes:
        """Read a line from the serial port."""
        return self._serial.readline()

    def is_open(self) -> bool:
        """Check if the serial port is open."""
        return self._serial.is_open

    def close(self):
        """Close the serial port."""
        if self._serial.is_open:
            self._serial.close()
            logger.debug("Serial port closed")

    def in_waiting(self) -> int:
        """Get the number of bytes waiting to be read."""
        return self._serial.in_waiting
