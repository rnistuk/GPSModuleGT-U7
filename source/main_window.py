import os

from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QStatusBar, QLineEdit, QMessageBox, QPushButton, QLabel,
    QFileDialog
)

from Panels.gps_status_panel import GPSStatusPanel
from Panels.panel_constants import (
    PANEL_STYLE, PANEL_WIDTH, PANEL_HEIGHT, TITLE_STYLE, TITLE_HEIGHT
)
from Panels.position_panel import PositionPanel
from Panels.satellite_panel import SatellitePanel
from app_config import AppConfig, DEFAULT_CONFIG
from command_formatter import MeshtasticCommandFormatter
from gps import GT_U7GPS
from gps_connection_manager import GPSConnectionManager
from gps_data_controller import GPSDataController
from gps_data_exporter import GPSDataExporter
from gps_update_controller import GPSUpdateController
from settings_dialog import SettingsDialog


class MainWindow(QMainWindow):
    def __init__(self, config: AppConfig = None, gps_instance: GT_U7GPS = None):
        """
        Initialize the main window.

        Args:
            config: Application configuration (uses DEFAULT_CONFIG if not provided)
            gps_instance: Optional pre-configured GPS instance for dependency injection
        """
        super().__init__()
        self.config = config or DEFAULT_CONFIG

        # Initialize connection manager
        self.connection_manager = GPSConnectionManager(
            port=self.config.gps_port,
            baudrate=self.config.baudrate,
            status_callback=self._update_status_bar
        )

        # Initialize data controller
        self.data_controller = GPSDataController(self.connection_manager)

        # Initialize data exporter
        self.data_exporter = GPSDataExporter()

        # Initialize command formatter
        self.command_formatter = MeshtasticCommandFormatter()

        # Initialize update controller
        self.update_controller = GPSUpdateController(
            update_interval_ms=self.config.gps_update_interval_ms,
            reconnect_interval_ms=self.config.gps_reconnect_interval_ms,
            update_callback=self.update_gps_data,
            reconnect_callback=self.connection_manager.reconnect
        )

        # Allow GPS instance injection (useful for testing)
        if gps_instance:
            self.connection_manager._gps = gps_instance
        else:
            self.connection_manager.connect()

        main_layout = self.init_view()
        self.update_controller.start()

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        self.show()

    def closeEvent(self, event):
        self.update_controller.stop()
        self.connection_manager.disconnect()
        event.accept()

    def _update_status_bar(self, message: str):
        """Callback for connection manager status updates."""
        if hasattr(self, 'status_bar'):
            self.status_bar.showMessage(message)

    # View
    def _format_meshtastic_command(self):
        """Format Meshtastic command using current GPS data."""
        gps_data = self.data_controller.get_current_data()
        return self.command_formatter.format(gps_data)

    def _create_quick_actions_panel(self) -> QWidget:
        """
        Create the Quick Actions panel with buttons.

        Returns:
            QWidget containing the Quick Actions panel
        """
        actions_widget = QWidget()
        actions_widget.setStyleSheet(PANEL_STYLE)
        actions_widget.setFixedWidth(PANEL_WIDTH)
        actions_widget.setFixedHeight(PANEL_HEIGHT)

        actions_inner_layout = QVBoxLayout()
        actions_title = QLabel("Quick Actions")
        actions_title.setStyleSheet(TITLE_STYLE)
        actions_title.setAlignment(QtCore.Qt.AlignCenter)
        actions_title.setFixedHeight(TITLE_HEIGHT)

        refresh_button = QPushButton("Refresh GPS")
        refresh_button.clicked.connect(self.manual_refresh)

        export_button = QPushButton("Export Data")
        export_button.clicked.connect(self.export_data)

        settings_button = QPushButton("Settings")
        settings_button.clicked.connect(self.open_settings)

        actions_inner_layout.addWidget(actions_title)
        actions_inner_layout.addWidget(refresh_button)
        actions_inner_layout.addWidget(export_button)
        actions_inner_layout.addWidget(settings_button)
        actions_inner_layout.setSpacing(2)
        actions_inner_layout.setContentsMargins(5, 0, 5, 5)
        actions_widget.setLayout(actions_inner_layout)

        return actions_widget

    def _create_command_section(self) -> QHBoxLayout:
        """
        Create the Meshtastic command section with copy button.

        Returns:
            QHBoxLayout containing the command field and copy button
        """
        self.meshtastic_command_field = QLineEdit()
        self.meshtastic_command_field.setFixedHeight(30)
        self.meshtastic_command_field.setReadOnly(True)
        self.meshtastic_command_field.setText(self._format_meshtastic_command())

        copy_button = QPushButton("Copy")
        copy_button.setFixedWidth(80)
        copy_button.clicked.connect(self.copy_command)

        command_layout = QHBoxLayout()
        command_layout.addWidget(self.meshtastic_command_field)
        command_layout.addWidget(copy_button)

        return command_layout

    def init_view(self):
        """Initialize the main window view with all UI components."""
        self.setWindowTitle("GT-U7 GPS")
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

        # Create panels
        self.position_panel = PositionPanel()
        self.satellite_panel = SatellitePanel()
        self.gps_status_panel = GPSStatusPanel()

        # Create Quick Actions panel
        actions_widget = self._create_quick_actions_panel()

        # Create grid layout for panels (2x2)
        panels_grid = QGridLayout()
        panels_grid.addWidget(self.position_panel, 0, 0)
        panels_grid.addWidget(self.satellite_panel, 0, 1)
        panels_grid.addWidget(self.gps_status_panel, 1, 0)
        panels_grid.addWidget(actions_widget, 1, 1)
        panels_grid.setSpacing(5)
        panels_grid.setColumnStretch(2, 1)

        # Create command section
        command_layout = self._create_command_section()

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(panels_grid)
        main_layout.addLayout(command_layout)

        self.update_position_panel()
        self.update_status_panels()
        return main_layout

    def copy_command(self):
        """Copy Meshtastic command to clipboard."""
        clipboard = QtCore.QCoreApplication.instance().clipboard()
        clipboard.setText(self.meshtastic_command_field.text())
        self.status_bar.showMessage("Command copied to clipboard!", 2000)

    def update_status_panels(self):
        """Update satellite and GPS status panels."""
        if self.data_controller.is_connected:
            sat_info = self.data_controller.get_satellite_info()
            self.satellite_panel.set_num_sats(sat_info['num_sats'])
            self.satellite_panel.set_fix_quality(sat_info['gps_quality'])
            self.gps_status_panel.set_connection_status(True)
            self.gps_status_panel.update_timestamp()
        else:
            self.gps_status_panel.set_connection_status(False)

    def manual_refresh(self):
        """Manually refresh GPS data."""
        success = self.data_controller.manual_refresh(
            status_callback=lambda msg: self.status_bar.showMessage(msg, 1000 if "Refreshing" in msg else 2000)
        )
        if success:
            self.update_gps_data()

    def export_data(self):
        """Export current GPS data to CSV file."""
        # Validate data availability
        is_valid, error_msg = self.data_controller.validate_export_data()
        if not is_valid:
            QMessageBox.warning(self, "Export Error", error_msg)
            return

        # Open file dialog
        default_filename = self.data_exporter.generate_default_filename()
        file_filter = self.data_exporter.get_file_filter()
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export GPS Data",
            default_filename,
            file_filter
        )

        if not filename:
            return  # User cancelled

        # Export data
        gps_data = self.data_controller.get_current_data()
        success, error_msg = self.data_exporter.export_to_file(gps_data, filename)

        if success:
            self.status_bar.showMessage(f"GPS data exported to {os.path.basename(filename)}", 3000)
            QMessageBox.information(self, "Export Successful",
                                    f"GPS data successfully exported to:\n{filename}")
        else:
            QMessageBox.critical(self, "Export Error", error_msg)
            self.status_bar.showMessage(f"Export failed: {error_msg}", 3000)

    def open_settings(self):
        """Open settings dialog."""
        dialog = SettingsDialog(
            self,
            current_port=self.connection_manager.port,
            current_baudrate=self.connection_manager.baudrate,
            update_interval=self.update_controller.update_interval,
            reconnect_interval=self.update_controller.reconnect_interval
        )

        if dialog.exec_() == SettingsDialog.Accepted:
            settings = dialog.get_settings()

            # Update intervals
            self.update_controller.set_update_interval(settings['update_interval'])
            self.update_controller.set_reconnect_interval(settings['reconnect_interval'])

            # Update connection parameters and reconnect
            self.connection_manager.update_connection_params(
                port=settings['port'],
                baudrate=settings['baudrate']
            )
            self.status_bar.showMessage("Settings saved. Reconnecting to GPS...", 2000)

    def update_position_panel(self):
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
            self.status_bar.showMessage(f"GPS Error: {e}")

    # Controller
    def update_gps_data(self):
        """Update GPS data and refresh UI - called by update controller."""
        if not self.data_controller.is_connected:
            if not self.connection_manager.is_reconnecting:
                self.update_controller.schedule_reconnect()
            self.status_bar.showMessage("The GPS Module is not connected.")
            return

        success = self.data_controller.update_gps_data()

        if success:
            self.update_position_panel()
            self.update_status_panels()
            self.meshtastic_command_field.setText(self._format_meshtastic_command())
            sat_info = self.data_controller.get_satellite_info()
            self.status_bar.showMessage(f"Number of Satellites: {sat_info['num_sats']}")
        else:
            error_msg = self.data_controller.last_error
            self.status_bar.showMessage(error_msg)
            self.update_controller.schedule_reconnect()
