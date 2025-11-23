"""
Protocol definitions for type-safe interfaces.

Defines contracts for callbacks and interfaces used throughout the application.
"""
from typing import Protocol, Optional, Dict, Any, Tuple
from gps_data import GPSData


class StatusCallbackProtocol(Protocol):
    """Protocol for status message callbacks."""

    def __call__(self, message: str, duration: int = 2000) -> None:
        """
        Display a status message.

        Args:
            message: The status message to display
            duration: Duration in milliseconds to show the message
        """
        ...


class SimpleStatusCallbackProtocol(Protocol):
    """Protocol for simple status message callbacks (no duration)."""

    def __call__(self, message: str) -> None:
        """
        Display a status message.

        Args:
            message: The status message to display
        """
        ...


class DataUpdateCallbackProtocol(Protocol):
    """Protocol for data update callbacks."""

    def __call__(self) -> None:
        """Execute data update."""
        ...


class ReconnectCallbackProtocol(Protocol):
    """Protocol for reconnection callbacks."""

    def __call__(self) -> bool:
        """
        Attempt to reconnect.

        Returns:
            True if reconnection successful, False otherwise
        """
        ...


class GPSDataProviderProtocol(Protocol):
    """
    Protocol for GPS data providers.

    Defines the interface for objects that can provide GPS data
    without exposing implementation details.
    """

    def get_current_data(self) -> Optional[GPSData]:
        """
        Get current GPS data.

        Returns:
            GPSData object or None if not available
        """
        ...

    def get_satellite_info(self) -> Dict[str, Any]:
        """
        Get satellite information.

        Returns:
            Dictionary with num_sats and gps_quality
        """
        ...

    def get_position_info(self) -> Dict[str, Any]:
        """
        Get position information.

        Returns:
            Dictionary with latitude, longitude, height and directions
        """
        ...

    def validate_export_data(self) -> Tuple[bool, Optional[str]]:
        """
        Validate that GPS data is available for export.

        Returns:
            Tuple of (is_valid, error_message)
        """
        ...

    @property
    def is_connected(self) -> bool:
        """Check if GPS is connected."""
        ...


class DataExporterProtocol(Protocol):
    """Protocol for data exporters."""

    def generate_default_filename(self) -> str:
        """
        Generate default filename for export.

        Returns:
            Default filename string
        """
        ...

    def get_file_filter(self) -> str:
        """
        Get file filter string for file dialog.

        Returns:
            File filter string
        """
        ...

    def export_to_file(self, gps_data: GPSData, filename: str) -> Tuple[bool, Optional[str]]:
        """
        Export GPS data to file.

        Args:
            gps_data: GPS data to export
            filename: Target filename

        Returns:
            Tuple of (success, error_message)
        """
        ...


class CommandFormatterProtocol(Protocol):
    """Protocol for command formatters."""

    def format(self, gps_data: Optional[GPSData]) -> str:
        """
        Format GPS data into a command string.

        Args:
            gps_data: GPS data to format

        Returns:
            Formatted command string
        """
        ...


class ConnectionManagerProtocol(Protocol):
    """Protocol for connection managers."""

    @property
    def port(self) -> str:
        """Get current port."""
        ...

    @property
    def baudrate(self) -> int:
        """Get current baudrate."""
        ...

    @property
    def is_connected(self) -> bool:
        """Check if connected."""
        ...

    @property
    def is_reconnecting(self) -> bool:
        """Check if reconnecting."""
        ...

    def connect(self) -> bool:
        """Connect to device."""
        ...

    def disconnect(self) -> None:
        """Disconnect from device."""
        ...

    def reconnect(self) -> bool:
        """Reconnect to device."""
        ...

    def update_connection_params(self, port: Optional[str] = None, baudrate: Optional[int] = None) -> None:
        """Update connection parameters."""
        ...


class UpdateControllerProtocol(Protocol):
    """Protocol for update controllers."""

    @property
    def update_interval(self) -> int:
        """Get update interval in milliseconds."""
        ...

    @property
    def reconnect_interval(self) -> int:
        """Get reconnect interval in milliseconds."""
        ...

    def start(self) -> None:
        """Start the update controller."""
        ...

    def stop(self) -> None:
        """Stop the update controller."""
        ...

    def schedule_reconnect(self) -> None:
        """Schedule a reconnection attempt."""
        ...

    def set_update_interval(self, interval_ms: int) -> None:
        """Set update interval."""
        ...

    def set_reconnect_interval(self, interval_ms: int) -> None:
        """Set reconnect interval."""
        ...
