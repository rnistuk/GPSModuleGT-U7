"""
Statistical analysis for GPS data with rolling window support.
"""
from collections import deque
from statistics import mean, median, mode, StatisticsError
from typing import Optional
from gps_data import GPSData


class GPSStatistics:
    """
    Maintains a rolling window of GPS data and provides real-time statistical analysis.

    Calculates statistics (mean, median, mode) for numerical fields: latitude, longitude, and height.
    """

    def __init__(self, N: Optional[int] = 10):
        """
        Initialize the Statistics class with a rolling window.

        Args:
            N: Maximum number of GPSData objects to store (default: 10)
        """
        self._data: deque = deque(maxlen=N)

    def add_data(self, gps_data: GPSData) -> None:
        """
        Add a new GPSData object to the rolling window.

        Args:
            gps_data: GPSData instance to add
        """
        self._data.append(gps_data)

    def get_mean(self) -> dict:
        """
        Calculate the arithmetic mean for latitude, longitude, and height.

        Returns:
            Dictionary with mean values for each field, or None if empty
        """
        if not self._data:
            return {'latitude': None, 'longitude': None, 'height': None}

        latitudes = [d.latitude for d in self._data]
        longitudes = [d.longitude for d in self._data]
        heights = [d.height for d in self._data]

        return {
            'latitude': mean(latitudes),
            'longitude': mean(longitudes),
            'height': mean(heights)
        }

    def get_median(self) -> dict:
        """
        Calculate the median for latitude, longitude, and height.

        Returns:
            Dictionary with median values for each field, or None if empty
        """
        if not self._data:
            return {'latitude': None, 'longitude': None, 'height': None}

        latitudes = [d.latitude for d in self._data]
        longitudes = [d.longitude for d in self._data]
        heights = [d.height for d in self._data]

        return {
            'latitude': median(latitudes),
            'longitude': median(longitudes),
            'height': median(heights)
        }

    def get_mode(self) -> dict:
        """
        Calculate the mode for latitude, longitude, and height.

        Handles multimodal data by returning None for fields with no unique mode.

        Returns:
            Dictionary with mode values for each field, or None if empty/no unique mode
        """
        if not self._data:
            return {'latitude': None, 'longitude': None, 'height': None}

        latitudes = [d.latitude for d in self._data]
        longitudes = [d.longitude for d in self._data]
        heights = [d.height for d in self._data]

        result = {}

        # Calculate mode for latitude
        try:
            result['latitude'] = mode(latitudes)
        except StatisticsError:
            result['latitude'] = None

        # Calculate mode for longitude
        try:
            result['longitude'] = mode(longitudes)
        except StatisticsError:
            result['longitude'] = None

        # Calculate mode for height
        try:
            result['height'] = mode(heights)
        except StatisticsError:
            result['height'] = None

        return result
