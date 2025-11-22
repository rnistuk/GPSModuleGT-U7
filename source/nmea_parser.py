"""
NMEA sentence parser for extracting GPS data.
Handles parsing and processing of NMEA 0183 protocol messages.
"""
import logging

import pynmea2

from source.gps_data import GPSData

logger = logging.getLogger(__name__)

NMEA_GPS_PREFIX = '$GP'


class NMEAParser:
    """
    Parser for NMEA 0183 GPS sentences.

    Extracts position, altitude, and satellite information from NMEA messages
    and updates a GPSData object.
    """

    def __init__(self, gps_data: GPSData):
        """
        Initialize NMEA parser.

        Args:
            gps_data: GPSData object to update with parsed information
        """
        self._data = gps_data

    def parse_sentence(self, nmea_sentence: str) -> bool:
        """
        Parse a single NMEA sentence and update GPS data.

        Args:
            nmea_sentence: Raw NMEA sentence string

        Returns:
            True if sentence was parsed successfully, False otherwise
        """
        if not nmea_sentence or not nmea_sentence.startswith(NMEA_GPS_PREFIX):
            return False

        try:
            logger.debug(f"NMEA: {nmea_sentence}")
            msg = pynmea2.parse(nmea_sentence)

            if hasattr(msg, 'timestamp'):
                logger.debug(f"Timestamp: {msg.timestamp}")

            self._process_position(msg)
            self._process_altitude(msg)
            self._process_satellites(msg)
            logger.debug("-" * 20)
            return True

        except pynmea2.ParseError as e:
            logger.error(f"Error parsing NMEA: {e}")
            return False

    def _process_position(self, msg):
        """Extract position data from NMEA message."""
        if hasattr(msg, 'latitude') and hasattr(msg, 'longitude'):
            self._data.latitude = msg.latitude
            self._data.longitude = msg.longitude
            self._data.lat_dir = msg.lat_dir
            self._data.lon_dir = msg.lon_dir
            logger.debug(f"Latitude: {msg.latitude}° {msg.lat_dir}")
            logger.debug(f"Longitude: {msg.longitude}° {msg.lon_dir}")

    def _process_altitude(self, msg):
        """Extract altitude data from NMEA message."""
        if hasattr(msg, 'altitude'):
            self._data.height = msg.altitude
            logger.debug(f"Altitude: {msg.altitude} {msg.altitude_units}")

    def _process_satellites(self, msg):
        """Extract satellite count and GPS quality from NMEA message."""
        if hasattr(msg, 'num_sats'):
            self._data.num_sats = int(msg.num_sats)
            logger.info(f"Satellites: {msg.num_sats}")
        if hasattr(msg, 'gps_qual'):
            self._data.gps_quality = int(msg.gps_qual)
            logger.debug(f"GPS Quality: {msg.gps_qual}")
