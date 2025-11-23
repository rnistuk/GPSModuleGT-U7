"""
View update coordinator for managing UI updates.
"""
from typing import Optional, Callable

from gps_data_controller import GPSDataController
from Panels.position_panel import PositionPanel
from Panels.satellite_panel import SatellitePanel
from Panels.gps_status_panel import GPSStatusPanel
from command_formatter import MeshtasticCommandFormatter


class ViewUpdateCoordinator:
    """
    Coordinator for updating all view components.

    Centralizes view update logic to maintain single responsibility
    and reduce complexity in MainWindow.
    """

    def __init__(self,
                 data_controller: GPSDataController,
                 position_panel: PositionPanel,
                 satellite_panel: SatellitePanel,
                 status_panel: GPSStatusPanel,
                 command_formatter: MeshtasticCommandFormatter,
                 command_field_updater: Optional[Callable[[str], None]] = None,
                 status_callback: Optional[Callable[[str], None]] = None):
        """
        Initialize view update coordinator.

        Args:
            data_controller: GPS data controller
            position_panel: Position display panel
            satellite_panel: Satellite info panel
            status_panel: GPS status panel
            command_formatter: Meshtastic command formatter
            command_field_updater: Callback to update command field (takes command string)
            status_callback: Callback for status bar messages
        """
        self.data_controller = data_controller
        self.position_panel = position_panel
        self.satellite_panel = satellite_panel
        self.status_panel = status_panel
        self.command_formatter = command_formatter
        self.command_field_updater = command_field_updater
        self.status_callback = status_callback

    def update_all(self) -> None:
        """
        Update all view components with current GPS data.

        This is the main coordination method that updates all panels,
        command field, and status bar in a single operation.
        """
        if not self.data_controller.is_connected:
            self._handle_disconnected_state()
            return

        # Update all panels
        self.update_position_panel()
        self.update_status_panels()
        self.update_command_field()

        # Update status bar
        sat_info = self.data_controller.get_satellite_info()
        if self.status_callback and sat_info['num_sats'] is not None:
            self.status_callback(f"Number of Satellites: {sat_info['num_sats']}")

    def update_position_panel(self) -> None:
        """Update position panel with current GPS position data."""
        if not self.data_controller.is_connected:
            return

        try:
            pos_info = self.data_controller.get_position_info()
            self.position_panel.set_position(
                pos_info['latitude'],
                pos_info['lat_dir'],
                pos_info['longitude'],
                pos_info['lon_dir'],
                pos_info['height']
            )
        except Exception as e:
            if self.status_callback:
                self.status_callback(f"GPS Error: {e}")

    def update_status_panels(self) -> None:
        """Update satellite and GPS status panels."""
        if self.data_controller.is_connected:
            sat_info = self.data_controller.get_satellite_info()
            self.satellite_panel.set_num_sats(sat_info['num_sats'])
            self.satellite_panel.set_fix_quality(sat_info['gps_quality'])
            self.status_panel.set_connection_status(True)
            self.status_panel.update_timestamp()
        else:
            self.status_panel.set_connection_status(False)

    def update_command_field(self) -> None:
        """Update Meshtastic command field with current GPS data."""
        if self.command_field_updater:
            gps_data = self.data_controller.get_current_data()
            command = self.command_formatter.format(gps_data)
            self.command_field_updater(command)

    def _handle_disconnected_state(self) -> None:
        """Handle UI updates when GPS is disconnected."""
        self.status_panel.set_connection_status(False)
        if self.status_callback:
            self.status_callback("The GPS Module is not connected.")
