"""
Facade for GPS controller operations.

Provides a unified, simplified interface to all GPS-related controllers,
reducing coupling and complexity in client code.
"""
from typing import Optional, Dict, Any, Tuple

from gps_data import GPSData
from gps_connection_manager import GPSConnectionManager
from gps_data_controller import GPSDataController
from gps_update_controller import GPSUpdateController
from settings_mediator import SettingsMediator
from protocols import (
    StatusCallbackProtocol,
    DataUpdateCallbackProtocol,
    ReconnectCallbackProtocol
)


class GPSControllerFacade:
    """
    Facade providing unified interface to GPS controllers.

    Simplifies interaction with multiple controllers by providing
    a single entry point for common operations.
    """

    def __init__(self,
                 connection_manager: GPSConnectionManager,
                 data_controller: GPSDataController,
                 update_controller: GPSUpdateController,
                 settings_mediator: SettingsMediator):
        """
        Initialize GPS controller facade.

        Args:
            connection_manager: GPS connection manager
            data_controller: GPS data controller
            update_controller: GPS update controller
            settings_mediator: Settings mediator
        """
        self._connection_manager = connection_manager
        self._data_controller = data_controller
        self._update_controller = update_controller
        self._settings_mediator = settings_mediator

    # Connection operations
    @property
    def is_connected(self) -> bool:
        """Check if GPS is connected."""
        return self._data_controller.is_connected

    @property
    def is_reconnecting(self) -> bool:
        """Check if GPS is reconnecting."""
        return self._settings_mediator.is_reconnecting()

    def inject_gps_instance(self, gps_instance) -> None:
        """
        Inject GPS instance (for testing).

        Args:
            gps_instance: GPS instance to inject
        """
        self._connection_manager._gps = gps_instance

    def connect(self) -> bool:
        """
        Connect to GPS device.

        Returns:
            True if successful
        """
        return self._connection_manager.connect()

    def disconnect(self) -> None:
        """Disconnect from GPS device."""
        self._connection_manager.disconnect()

    # Data operations
    def get_current_data(self) -> Optional[GPSData]:
        """
        Get current GPS data.

        Returns:
            GPSData object or None
        """
        return self._data_controller.get_current_data()

    def get_satellite_info(self) -> Dict[str, Any]:
        """
        Get satellite information.

        Returns:
            Dictionary with num_sats and gps_quality
        """
        return self._data_controller.get_satellite_info()

    def get_position_info(self) -> Dict[str, Any]:
        """
        Get position information.

        Returns:
            Dictionary with latitude, longitude, height and directions
        """
        return self._data_controller.get_position_info()

    def update_gps_data(self) -> bool:
        """
        Update GPS data from device.

        Returns:
            True if successful, False otherwise
        """
        return self._data_controller.update_gps_data()

    def manual_refresh(self, status_callback: Optional[StatusCallbackProtocol] = None) -> bool:
        """
        Manually refresh GPS data.

        Args:
            status_callback: Optional callback for status messages

        Returns:
            True if successful
        """
        # Convert StatusCallbackProtocol to SimpleStatusCallbackProtocol
        simple_callback = None
        if status_callback:
            def simple_callback(msg: str):
                duration = 1000 if "Refreshing" in msg else 2000
                status_callback(msg, duration)

        return self._data_controller.manual_refresh(status_callback=simple_callback)

    def validate_export_data(self) -> Tuple[bool, Optional[str]]:
        """
        Validate that GPS data is available for export.

        Returns:
            Tuple of (is_valid, error_message)
        """
        return self._data_controller.validate_export_data()

    @property
    def last_error(self) -> Optional[str]:
        """Get last error message."""
        return self._data_controller.last_error

    # Update controller operations
    def start_updates(self) -> None:
        """Start automatic GPS updates."""
        self._update_controller.start()

    def stop_updates(self) -> None:
        """Stop automatic GPS updates."""
        self._update_controller.stop()

    def schedule_reconnect(self) -> None:
        """Schedule a reconnection attempt."""
        self._update_controller.schedule_reconnect()

    def set_update_callbacks(self,
                            update_callback: Optional[DataUpdateCallbackProtocol] = None,
                            reconnect_callback: Optional[ReconnectCallbackProtocol] = None) -> None:
        """
        Set update callbacks (used during initialization).

        Args:
            update_callback: Callback for data updates
            reconnect_callback: Callback for reconnection
        """
        # Note: This is typically set during UpdateController initialization
        # This method is here for completeness but may not be commonly used
        pass

    # Settings operations
    def get_current_settings(self) -> Dict[str, Any]:
        """
        Get current application settings.

        Returns:
            Dictionary with all settings
        """
        return self._settings_mediator.get_current_settings()

    def apply_settings(self, settings: Dict[str, Any], callback: Optional[callable] = None) -> None:
        """
        Apply new settings.

        Args:
            settings: Dictionary with new settings
            callback: Optional callback for status updates
        """
        self._settings_mediator.apply_settings(settings, callback)

    # Direct controller access (for special cases)
    @property
    def connection_manager(self) -> GPSConnectionManager:
        """Get connection manager (use sparingly)."""
        return self._connection_manager

    @property
    def data_controller(self) -> GPSDataController:
        """Get data controller (use sparingly)."""
        return self._data_controller

    @property
    def update_controller(self) -> GPSUpdateController:
        """Get update controller (use sparingly)."""
        return self._update_controller

    @property
    def settings_mediator(self) -> SettingsMediator:
        """Get settings mediator (use sparingly)."""
        return self._settings_mediator
