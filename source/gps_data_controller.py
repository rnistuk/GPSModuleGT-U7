"""
GPS Data Controller for managing GPS data updates and business logic.
Separates controller concerns from view logic.
"""
import logging
from typing import Optional, Callable, Dict, Any

from gps_connection_manager import GPSConnectionManager
from gps_data import GPSData

logger = logging.getLogger(__name__)


class GPSDataController:
    """
    Controller for GPS data operations and business logic.

    Handles GPS data reading, error handling, and provides a clean
    interface for the view layer without exposing GPS implementation details.
    """

    def __init__(self, connection_manager: GPSConnectionManager):
        """
        Initialize GPS data controller.

        Args:
            connection_manager: GPS connection manager instance
        """
        self.connection_manager = connection_manager
        self._last_error: Optional[str] = None

    @property
    def is_connected(self) -> bool:
        """Check if GPS is connected."""
        return self.connection_manager.is_connected

    @property
    def last_error(self) -> Optional[str]:
        """Get last error message."""
        return self._last_error

    def get_current_data(self) -> Optional[GPSData]:
        """
        Get current GPS data without updating.

        Returns:
            Current GPSData object or None if not connected
        """
        gps = self.connection_manager.gps
        if not gps:
            return None
        return gps.data

    def get_satellite_info(self) -> Dict[str, Any]:
        """
        Get satellite information.

        Returns:
            Dictionary with num_sats and gps_quality, or None values if not connected
        """
        gps = self.connection_manager.gps
        if not gps:
            return {'num_sats': None, 'gps_quality': None}
        return {
            'num_sats': gps.num_sats,
            'gps_quality': gps.gps_quality
        }

    def get_position_info(self) -> Dict[str, Any]:
        """
        Get position information.

        Returns:
            Dictionary with latitude, longitude, height and directions, or None values if not connected
        """
        gps = self.connection_manager.gps
        if not gps:
            return {
                'latitude': None,
                'longitude': None,
                'lat_dir': None,
                'lon_dir': None,
                'height': None
            }
        return {
            'latitude': gps.latitude,
            'longitude': gps.longitude,
            'lat_dir': gps.lat_dir,
            'lon_dir': gps.lon_dir,
            'height': gps.height
        }

    def update_gps_data(self) -> bool:
        """
        Read and update GPS data from device.

        Returns:
            True if update successful, False otherwise

        Side effects:
            Sets self._last_error on failure
        """
        self._last_error = None

        gps = self.connection_manager.gps
        if not gps:
            self._last_error = "The GPS Module is not connected."
            return False

        try:
            gps.read_gps_data()
            return True
        except RuntimeError as e:
            self._last_error = f"GPS Error: {e}"
            logger.error(f"GPS read error: {e}")
            # Disconnect on read error to trigger reconnection
            self.connection_manager.disconnect()
            return False

    def manual_refresh(self, status_callback: Optional[Callable[[str], None]] = None) -> bool:
        """
        Manually refresh GPS data.

        Args:
            status_callback: Optional callback for status messages

        Returns:
            True if refresh successful, False otherwise
        """
        if self.connection_manager.is_connected:
            if status_callback:
                status_callback("Refreshing GPS data...")
            return self.update_gps_data()
        else:
            if status_callback:
                status_callback("GPS not connected. Attempting reconnection...")
            return self.connection_manager.reconnect()

    def validate_export_data(self) -> tuple[bool, Optional[str]]:
        """
        Validate that GPS data is available for export.

        Returns:
            Tuple of (is_valid, error_message)
        """
        gps = self.connection_manager.gps
        if not gps:
            return False, "No GPS data available to export."

        data = gps.data
        if not data or not data.has_position():
            return False, "GPS data is not valid or has no position information."

        return True, None
