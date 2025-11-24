from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStatusBar, QLineEdit, QPushButton, QLabel
)

from Panels.panel_constants import (
    PANEL_STYLE, PANEL_WIDTH, PANEL_HEIGHT, TITLE_STYLE, TITLE_HEIGHT
)
from actions import RefreshAction, ExportAction, SettingsAction
from app_config import AppConfig, DEFAULT_CONFIG
from command_formatter import MeshtasticCommandFormatter
from gps import GT_U7GPS
from gps_connection_manager import GPSConnectionManager
from gps_controller_facade import GPSControllerFacade
from gps_data_controller import GPSDataController
from gps_data_exporter import GPSDataExporter
from gps_update_controller import GPSUpdateController
from panel_factory import PanelFactory
from settings_mediator import SettingsMediator
from view_update_coordinator import ViewUpdateCoordinator


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

        # Initialize managers and controllers
        self.connection_manager = GPSConnectionManager(
            port=self.config.gps_port,
            baudrate=self.config.baudrate,
            status_callback=self._update_status_bar
        )
        self.data_controller = GPSDataController(self.connection_manager)
        self.data_exporter = GPSDataExporter()
        self.command_formatter = MeshtasticCommandFormatter()
        self.update_controller = GPSUpdateController(
            update_interval_ms=self.config.gps_update_interval_ms,
            reconnect_interval_ms=self.config.gps_reconnect_interval_ms,
            update_callback=self.update_gps_data,
            reconnect_callback=self.connection_manager.reconnect
        )

        # Initialize mediators and coordinators
        self.settings_mediator = SettingsMediator(
            self.connection_manager,
            self.update_controller
        )
        self.panel_factory = PanelFactory()

        # Initialize GPS facade
        self.gps_facade = GPSControllerFacade(
            connection_manager=self.connection_manager,
            data_controller=self.data_controller,
            update_controller=self.update_controller,
            settings_mediator=self.settings_mediator
        )

        # Allow GPS instance injection (useful for testing)
        if gps_instance:
            self.gps_facade.inject_gps_instance(gps_instance)
        else:
            self.gps_facade.connect()

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

    # View helpers
    def _status_message(self, message: str, duration: int = 2000):
        """Helper to show status bar message."""
        self.status_bar.showMessage(message, duration)

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

        # Set command field updater in view coordinator
        if hasattr(self, 'view_coordinator'):
            self.view_coordinator.command_field_updater = self.meshtastic_command_field.setText

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

        # Create Quick Actions panel
        actions_widget = self._create_quick_actions_panel()

        # Create panels using factory
        panels_grid = self.panel_factory.create_default_layout(actions_widget)

        # Get panel references
        self.position_panel = self.panel_factory.get_panel(PanelFactory.POSITION_PANEL)
        self.satellite_panel = self.panel_factory.get_panel(PanelFactory.SATELLITE_PANEL)
        self.gps_status_panel = self.panel_factory.get_panel(PanelFactory.STATUS_PANEL)

        # Initialize view update coordinator
        self.view_coordinator = ViewUpdateCoordinator(
            data_controller=self.data_controller,
            position_panel=self.position_panel,
            satellite_panel=self.satellite_panel,
            status_panel=self.gps_status_panel,
            command_formatter=self.command_formatter,
            command_field_updater=None,  # Will be set after command field is created
            status_callback=self._status_message
        )

        # Create command section
        command_layout = self._create_command_section()

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(panels_grid)
        main_layout.addLayout(command_layout)

        # Initial update
        self.view_coordinator.update_all()
        return main_layout

    def copy_command(self):
        """Copy Meshtastic command to clipboard."""
        clipboard = QtCore.QCoreApplication.instance().clipboard()
        clipboard.setText(self.meshtastic_command_field.text())
        self._status_message("Command copied to clipboard!", 2000)

    # Action handlers
    def manual_refresh(self):
        """Manually refresh GPS data."""
        action = RefreshAction(
            data_controller=self.data_controller,
            status_callback=self._status_message,
            success_callback=self.update_gps_data
        )
        action.execute()

    def export_data(self):
        """Export current GPS data to CSV file."""
        action = ExportAction(
            data_controller=self.data_controller,
            data_exporter=self.data_exporter,
            parent_widget=self,
            status_callback=self._status_message
        )
        action.execute()

    def open_settings(self):
        """Open settings dialog."""
        action = SettingsAction(
            settings_mediator=self.settings_mediator,
            parent_widget=self,
            status_callback=self._status_message
        )
        action.execute()

    # Controller
    def update_gps_data(self):
        """Update GPS data and refresh UI - called by update controller."""
        if not self.data_controller.is_connected:
            if not self.settings_mediator.is_reconnecting():
                self.update_controller.schedule_reconnect()
            self._status_message("The GPS Module is not connected.")
            return

        success = self.data_controller.update_gps_data()

        if success:
            # Use coordinator for all view updates
            self.view_coordinator.update_all()
        else:
            error_msg = self.data_controller.last_error
            self._status_message(error_msg)
            self.update_controller.schedule_reconnect()
