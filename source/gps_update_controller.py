"""
GPS Update Controller for managing periodic GPS data updates.
Handles timer management and coordinates GPS reading with UI updates.
"""
import logging
from typing import Callable

from PyQt5 import QtCore

logger = logging.getLogger(__name__)


class GPSUpdateController:
    """
    Controls periodic GPS data updates.

    Manages a QTimer for regular GPS data reading and provides
    callback mechanism for UI updates.
    """

    def __init__(
            self,
            update_interval_ms: int,
            reconnect_interval_ms: int,
            update_callback: Callable[[], None],
            reconnect_callback: Callable[[], None]
    ):
        """
        Initialize GPS update controller.

        Args:
            update_interval_ms: How often to read GPS data (milliseconds)
            reconnect_interval_ms: How often to attempt reconnection (milliseconds)
            update_callback: Function to call on each update cycle
            reconnect_callback: Function to call when reconnection needed
        """
        self.update_interval = update_interval_ms
        self.reconnect_interval = reconnect_interval_ms
        self.update_callback = update_callback
        self.reconnect_callback = reconnect_callback

        # Create timer for regular updates
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.update_interval)
        self.timer.timeout.connect(self._on_timer_tick)

    def start(self):
        """Start the update timer."""
        if not self.timer.isActive():
            self.timer.start()
            logger.info(f"GPS update controller started with {self.update_interval}ms interval")

    def stop(self):
        """Stop the update timer."""
        if self.timer.isActive():
            self.timer.stop()
            logger.info("GPS update controller stopped")

    def is_running(self) -> bool:
        """Check if update timer is running."""
        return self.timer.isActive()

    def set_update_interval(self, interval_ms: int):
        """
        Change the update interval.

        Args:
            interval_ms: New update interval in milliseconds
        """
        was_running = self.timer.isActive()
        self.timer.stop()
        self.update_interval = interval_ms
        self.timer.setInterval(interval_ms)
        if was_running:
            self.timer.start()
        logger.info(f"Update interval changed to {interval_ms}ms")

    def set_reconnect_interval(self, interval_ms: int):
        """
        Change the reconnection interval.

        Args:
            interval_ms: New reconnection interval in milliseconds
        """
        self.reconnect_interval = interval_ms
        logger.info(f"Reconnect interval changed to {interval_ms}ms")

    def schedule_reconnect(self):
        """Schedule a reconnection attempt after reconnect_interval."""
        QtCore.QTimer.singleShot(self.reconnect_interval, self.reconnect_callback)
        logger.debug(f"Reconnection scheduled in {self.reconnect_interval}ms")

    def _on_timer_tick(self):
        """Internal timer callback - delegates to update callback."""
        self.update_callback()
