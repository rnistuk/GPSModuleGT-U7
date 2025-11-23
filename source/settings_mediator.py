"""
Settings mediator for managing application settings.
"""
from typing import Dict, Any, Optional, Callable

from gps_connection_manager import GPSConnectionManager
from gps_update_controller import GPSUpdateController


class SettingsMediator:
    """
    Mediator for coordinating settings across multiple controllers.

    Provides a unified interface for getting and setting application
    configuration without exposing controller internals.
    """

    def __init__(self,
                 connection_manager: GPSConnectionManager,
                 update_controller: GPSUpdateController):
        """
        Initialize settings mediator.

        Args:
            connection_manager: GPS connection manager
            update_controller: GPS update controller
        """
        self.connection_manager = connection_manager
        self.update_controller = update_controller

    def get_current_settings(self) -> Dict[str, Any]:
        """
        Get current application settings.

        Returns:
            Dictionary containing all current settings
        """
        return {
            'port': self.connection_manager.port,
            'baudrate': self.connection_manager.baudrate,
            'update_interval': self.update_controller.update_interval,
            'reconnect_interval': self.update_controller.reconnect_interval
        }

    def apply_settings(self,
                       settings: Dict[str, Any],
                       callback: Optional[Callable[[str], None]] = None) -> None:
        """
        Apply new settings to all controllers.

        Args:
            settings: Dictionary with new settings
            callback: Optional callback for status updates
        """
        # Update timing intervals
        if 'update_interval' in settings:
            self.update_controller.set_update_interval(settings['update_interval'])

        if 'reconnect_interval' in settings:
            self.update_controller.set_reconnect_interval(settings['reconnect_interval'])

        # Update connection parameters (triggers reconnect)
        connection_changed = False
        if 'port' in settings or 'baudrate' in settings:
            self.connection_manager.update_connection_params(
                port=settings.get('port'),
                baudrate=settings.get('baudrate')
            )
            connection_changed = True

        # Notify callback if provided
        if callback and connection_changed:
            callback("Settings applied. Reconnecting to GPS...")

    def get_connection_info(self) -> Dict[str, Any]:
        """
        Get connection-related settings only.

        Returns:
            Dictionary with port and baudrate
        """
        return {
            'port': self.connection_manager.port,
            'baudrate': self.connection_manager.baudrate
        }

    def get_timing_info(self) -> Dict[str, Any]:
        """
        Get timing-related settings only.

        Returns:
            Dictionary with update and reconnect intervals
        """
        return {
            'update_interval': self.update_controller.update_interval,
            'reconnect_interval': self.update_controller.reconnect_interval
        }

    def is_reconnecting(self) -> bool:
        """
        Check if GPS is currently reconnecting.

        Returns:
            True if reconnection in progress
        """
        return self.connection_manager.is_reconnecting
