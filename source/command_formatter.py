"""
Command Formatter for generating GPS-related commands.
Formats GPS data into various command formats (Meshtastic, etc.).
"""
from abc import ABC, abstractmethod
from typing import Optional

from gps_data import GPSData


class CommandFormatter(ABC):
    """Abstract base class for command formatters."""

    @abstractmethod
    def format(self, gps_data: Optional[GPSData]) -> str:
        """
        Format GPS data into a command string.

        Args:
            gps_data: GPS data to format (None if no data available)

        Returns:
            Formatted command string
        """
        pass

    @abstractmethod
    def get_placeholder(self) -> str:
        """
        Get placeholder string when GPS data is unavailable.

        Returns:
            Placeholder command string
        """
        pass


class MeshtasticCommandFormatter(CommandFormatter):
    """
    Formats GPS data into Meshtastic CLI commands.

    Meshtastic is a project for long-range mesh networking.
    """

    def format(self, gps_data: Optional[GPSData]) -> str:
        """
        Format GPS data into Meshtastic command.

        Args:
            gps_data: GPS data to format

        Returns:
            Meshtastic command string
        """
        if not gps_data or not gps_data.has_position():
            return self.get_placeholder()

        return (f"meshtastic --setlat {gps_data.latitude} "
                f"--setlon {gps_data.longitude} "
                f"--setalt {gps_data.height}")

    def get_placeholder(self) -> str:
        """
        Get placeholder Meshtastic command.

        Returns:
            Placeholder command string
        """
        return "meshtastic --setlat N/A --setlon N/A --setalt N/A"


class NMEACommandFormatter(CommandFormatter):
    """
    Formats GPS data into NMEA sentence format.

    Example output: $GPGGA sentence
    """

    def format(self, gps_data: Optional[GPSData]) -> str:
        """
        Format GPS data into NMEA GGA sentence.

        Args:
            gps_data: GPS data to format

        Returns:
            NMEA GGA sentence string
        """
        if not gps_data or not gps_data.has_position():
            return self.get_placeholder()

        # Simplified NMEA GGA format (without checksum for display)
        lat_deg = int(abs(gps_data.latitude))
        lat_min = (abs(gps_data.latitude) - lat_deg) * 60
        lat_dir = gps_data.lat_dir or ('N' if gps_data.latitude >= 0 else 'S')

        lon_deg = int(abs(gps_data.longitude))
        lon_min = (abs(gps_data.longitude) - lon_deg) * 60
        lon_dir = gps_data.lon_dir or ('E' if gps_data.longitude >= 0 else 'W')

        return (f"$GPGGA,{lat_deg:02d}{lat_min:07.4f},{lat_dir},"
                f"{lon_deg:03d}{lon_min:07.4f},{lon_dir},"
                f"Alt:{gps_data.height:.1f}m,Sats:{gps_data.num_sats}")

    def get_placeholder(self) -> str:
        """
        Get placeholder NMEA sentence.

        Returns:
            Placeholder NMEA string
        """
        return "$GPGGA,N/A,N/A,N/A"


class SimpleCommandFormatter(CommandFormatter):
    """
    Formats GPS data into simple coordinate string.

    Example: "Lat: 48.4034, Lon: -123.5448, Alt: 114.1m"
    """

    def format(self, gps_data: Optional[GPSData]) -> str:
        """
        Format GPS data into simple coordinate string.

        Args:
            gps_data: GPS data to format

        Returns:
            Simple coordinate string
        """
        if not gps_data or not gps_data.has_position():
            return self.get_placeholder()

        return (f"Lat: {gps_data.latitude:.4f}°, "
                f"Lon: {gps_data.longitude:.4f}°, "
                f"Alt: {gps_data.height:.1f}m")

    def get_placeholder(self) -> str:
        """
        Get placeholder coordinate string.

        Returns:
            Placeholder string
        """
        return "Lat: N/A, Lon: N/A, Alt: N/A"
