"""
Refresh GPS data action.
"""
from typing import Optional
from .base_action import BaseAction
from protocols import StatusCallbackProtocol, DataUpdateCallbackProtocol


class RefreshAction(BaseAction):
    """
    Action to manually refresh GPS data.

    Handles both connected and disconnected states, triggering
    reconnection when necessary.
    """

    def __init__(self,
                 data_controller,  # GPSDataController or compatible
                 status_callback: Optional[StatusCallbackProtocol] = None,
                 success_callback: Optional[DataUpdateCallbackProtocol] = None):
        """
        Initialize refresh action.

        Args:
            data_controller: GPS data controller instance
            status_callback: Callback for status messages
            success_callback: Callback to execute on successful refresh
        """
        self.data_controller = data_controller
        self.status_callback = status_callback
        self.success_callback = success_callback

    def execute(self) -> None:
        """Execute the refresh action."""
        success = self.data_controller.manual_refresh(
            status_callback=self._handle_status_message
        )

        if success and self.success_callback:
            self.success_callback()

    def _handle_status_message(self, message: str) -> None:
        """
        Handle status messages from the controller.

        Args:
            message: Status message to display
        """
        if self.status_callback:
            # Determine display duration based on message type
            duration = 1000 if "Refreshing" in message else 2000
            self.status_callback(message, duration)
