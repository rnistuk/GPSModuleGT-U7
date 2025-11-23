"""
Settings action for opening and applying settings.
"""
from typing import Callable, Optional
from PyQt5.QtWidgets import QWidget

from .base_action import BaseAction
from settings_dialog import SettingsDialog
from settings_mediator import SettingsMediator


class SettingsAction(BaseAction):
    """
    Action to open settings dialog and apply changes.

    Handles settings dialog display and delegates settings
    application to the SettingsMediator.
    """

    def __init__(self,
                 settings_mediator: SettingsMediator,
                 parent_widget: Optional[QWidget] = None,
                 status_callback: Optional[Callable[[str, int], None]] = None):
        """
        Initialize settings action.

        Args:
            settings_mediator: Settings mediator for managing settings
            parent_widget: Parent widget for dialog
            status_callback: Callback for status messages (message, duration)
        """
        self.settings_mediator = settings_mediator
        self.parent_widget = parent_widget
        self.status_callback = status_callback

    def execute(self) -> None:
        """Execute the settings action."""
        # Get current settings
        current_settings = self.settings_mediator.get_current_settings()

        # Show dialog
        dialog = SettingsDialog(
            self.parent_widget,
            current_port=current_settings['port'],
            current_baudrate=current_settings['baudrate'],
            update_interval=current_settings['update_interval'],
            reconnect_interval=current_settings['reconnect_interval']
        )

        # Apply settings if accepted
        if dialog.exec_() == SettingsDialog.Accepted:
            new_settings = dialog.get_settings()

            # Apply settings via mediator with callback
            def status_update(msg: str):
                if self.status_callback:
                    self.status_callback(msg, 2000)

            self.settings_mediator.apply_settings(new_settings, callback=status_update)
