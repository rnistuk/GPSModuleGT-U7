"""
GPS data model for storing position, altitude, and satellite information.
"""
from dataclasses import dataclass


@dataclass
class GPSData:
    """
    Data model for GPS position and status information.

    Attributes:
        latitude: Latitude in decimal degrees
        longitude: Longitude in decimal degrees
        lat_dir: Latitude direction ('N' or 'S')
        lon_dir: Longitude direction ('E' or 'W')
        height: Altitude/height in meters
        num_sats: Number of satellites in view
        gps_quality: GPS fix quality (0=Invalid, 1=GPS, 2=DGPS)
    """
    latitude: float = 0.0
    longitude: float = 0.0
    lat_dir: str = ''
    lon_dir: str = ''
    height: float = 0.0
    num_sats: int = 0
    gps_quality: int = 0

    def is_valid(self) -> bool:
        """Check if GPS has a valid fix."""
        return self.gps_quality > 0 and self.num_sats > 0

    def has_position(self) -> bool:
        """Check if position data is available."""
        return self.latitude != 0.0 or self.longitude != 0.0

    def to_dict(self) -> dict:
        """Convert GPS data to dictionary for export."""
        return {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'lat_dir': self.lat_dir,
            'lon_dir': self.lon_dir,
            'height': self.height,
            'num_sats': self.num_sats,
            'gps_quality': self.gps_quality
        }
