"""
GPS Connection Manager for handling GPS device lifecycle.
Manages connection, reconnection, and disconnection logic.
"""
import logging
from typing import Optional, Callable

from gps import GT_U7GPS

logger = logging.getLogger(__name__)


class GPSConnectionManager:
    """
    Manages GPS device connection lifecycle.

    Handles connecting, reconnecting, and disconnecting from GPS hardware,
    providing callbacks for status updates.
    """

    def __init__(self, port: str, baudrate: int, status_callback: Callable[[str], None] = None):
        """
        Initialize GPS connection manager.

        Args:
            port: Serial port path for GPS device
            baudrate: Serial communication speed
            status_callback: Optional callback function for status messages
        """
        self.port = port
        self.baudrate = baudrate
        self.status_callback = status_callback
        self._gps: Optional[GT_U7GPS] = None
        self._reconnecting = False

    @property
    def gps(self) -> Optional[GT_U7GPS]:
        """Get current GPS instance."""
        return self._gps

    @property
    def is_connected(self) -> bool:
        """Check if GPS is currently connected."""
        return self._gps is not None

    @property
    def is_reconnecting(self) -> bool:
        """Check if currently attempting to reconnect."""
        return self._reconnecting

    def inject_gps_instance(self, gps_instance: GT_U7GPS) -> None:
        """
        Inject GPS instance for testing.

        Args:
            gps_instance: GPS instance to inject
        """
        self._gps = gps_instance

    def connect(self) -> bool:
        """
        Attempt to connect to GPS device.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            self._gps = GT_U7GPS(port=self.port, baudrate=self.baudrate)
            logger.info(f"GPS connected on {self.port} at {self.baudrate} baud")
            self._notify_status("GPS connected successfully!")
            return True
        except RuntimeError as e:
            logger.error(f"Failed to connect to GPS: {e}")
            self._notify_status(f"GPS connection failed: {e}")
            self._gps = None
            return False

    def disconnect(self):
        """Disconnect from GPS device."""
        if self._gps:
            self._gps.close()
            self._gps = None
            logger.info("GPS disconnected")
            self._notify_status("GPS disconnected")

    def reconnect(self) -> bool:
        """
        Attempt to reconnect to GPS device.

        Returns:
            True if reconnection successful, False otherwise
        """
        if self._reconnecting:
            logger.debug("Reconnection already in progress")
            return False

        self._reconnecting = True
        self._notify_status("Attempting to reconnect to GPS...")
        logger.info("Attempting GPS reconnection...")

        # Disconnect existing connection if any
        self.disconnect()

        # Attempt new connection
        success = self.connect()

        self._reconnecting = False

        if success:
            logger.info("GPS reconnection successful")
            self._notify_status("GPS reconnected successfully!")
        else:
            logger.warning("GPS reconnection failed")
            self._notify_status("GPS reconnection failed")

        return success

    def update_connection_params(self, port: str = None, baudrate: int = None):
        """
        Update connection parameters and reconnect.

        Args:
            port: New serial port (optional, keeps current if None)
            baudrate: New baudrate (optional, keeps current if None)
        """
        if port is not None:
            self.port = port
        if baudrate is not None:
            self.baudrate = baudrate

        logger.info(f"Connection parameters updated: {self.port} @ {self.baudrate} baud")
        self.reconnect()

    def _notify_status(self, message: str):
        """
        Send status message via callback if available.

        Args:
            message: Status message to send
        """
        if self.status_callback:
            self.status_callback(message)
