"""
Panel factory for creating and managing GPS UI panels.
"""
from typing import Dict, List, Tuple
from PyQt5.QtWidgets import QWidget, QGridLayout

from Panels.position_panel import PositionPanel
from Panels.satellite_panel import SatellitePanel
from Panels.gps_status_panel import GPSStatusPanel


class PanelFactory:
    """
    Factory for creating GPS UI panels.

    Decouples panel creation from MainWindow and provides
    a registry for managing panels dynamically.
    """

    # Panel type constants
    POSITION_PANEL = "position"
    SATELLITE_PANEL = "satellite"
    STATUS_PANEL = "status"

    def __init__(self):
        """Initialize the panel factory."""
        self._panels: Dict[str, QWidget] = {}
        self._creation_registry = {
            self.POSITION_PANEL: self._create_position_panel,
            self.SATELLITE_PANEL: self._create_satellite_panel,
            self.STATUS_PANEL: self._create_status_panel
        }

    def create_panel(self, panel_type: str) -> QWidget:
        """
        Create a panel of the specified type.

        Args:
            panel_type: Type of panel to create

        Returns:
            Created panel widget

        Raises:
            ValueError: If panel type is not recognized
        """
        if panel_type not in self._creation_registry:
            raise ValueError(f"Unknown panel type: {panel_type}")

        panel = self._creation_registry[panel_type]()
        self._panels[panel_type] = panel
        return panel

    def get_panel(self, panel_type: str) -> QWidget:
        """
        Get an existing panel by type.

        Args:
            panel_type: Type of panel to retrieve

        Returns:
            Panel widget or None if not found
        """
        return self._panels.get(panel_type)

    def create_default_layout(self, actions_widget: QWidget) -> QGridLayout:
        """
        Create the default 2x2 panel grid layout.

        Args:
            actions_widget: Quick actions widget for bottom-right

        Returns:
            Configured grid layout with all panels
        """
        # Create panels
        position_panel = self.create_panel(self.POSITION_PANEL)
        satellite_panel = self.create_panel(self.SATELLITE_PANEL)
        status_panel = self.create_panel(self.STATUS_PANEL)

        # Create grid layout
        grid = QGridLayout()
        grid.addWidget(position_panel, 0, 0)
        grid.addWidget(satellite_panel, 0, 1)
        grid.addWidget(status_panel, 1, 0)
        grid.addWidget(actions_widget, 1, 1)
        grid.setSpacing(5)
        grid.setColumnStretch(2, 1)

        return grid

    def get_all_panels(self) -> Dict[str, QWidget]:
        """
        Get all created panels.

        Returns:
            Dictionary mapping panel types to panel widgets
        """
        return self._panels.copy()

    # Panel creation methods
    def _create_position_panel(self) -> PositionPanel:
        """Create position panel."""
        return PositionPanel()

    def _create_satellite_panel(self) -> SatellitePanel:
        """Create satellite panel."""
        return SatellitePanel()

    def _create_status_panel(self) -> GPSStatusPanel:
        """Create GPS status panel."""
        return GPSStatusPanel()
