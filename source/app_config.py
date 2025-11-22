"""
Application configuration for the GPS application.
Centralizes all configurable parameters.
"""
import os
from dataclasses import dataclass


@dataclass
class AppConfig:
    """
    Configuration parameters for the GPS application.

    Attributes:
        gps_port: Serial port path for GPS device
        baudrate: Serial communication speed
        gps_update_interval_ms: How often to read GPS data (milliseconds)
        gps_reconnect_interval_ms: How often to attempt reconnection (milliseconds)
    """
    gps_port: str = '/dev/cu.usbmodem2101'
    baudrate: int = 9600
    gps_update_interval_ms: int = 100
    gps_reconnect_interval_ms: int = 5000

    @staticmethod
    def from_environment() -> 'AppConfig':
        """
        Create configuration from environment variables.

        Environment variables:
            GPS_PORT: Override default GPS serial port
            GPS_BAUDRATE: Override default baudrate
            GPS_UPDATE_INTERVAL_MS: Override GPS update interval
            GPS_RECONNECT_INTERVAL_MS: Override reconnection interval

        Returns:
            AppConfig instance with values from environment or defaults
        """
        return AppConfig(
            gps_port=os.environ.get('GPS_PORT', '/dev/cu.usbmodem2101'),
            baudrate=int(os.environ.get('GPS_BAUDRATE', '9600')),
            gps_update_interval_ms=int(os.environ.get('GPS_UPDATE_INTERVAL_MS', '100')),
            gps_reconnect_interval_ms=int(os.environ.get('GPS_RECONNECT_INTERVAL_MS', '5000'))
        )


# Default configuration
DEFAULT_CONFIG = AppConfig()
