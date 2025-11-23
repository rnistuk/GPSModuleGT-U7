"""
Export GPS data action.
"""
import os
from typing import Optional
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget

from .base_action import BaseAction
from protocols import GPSDataProviderProtocol, DataExporterProtocol, StatusCallbackProtocol


class ExportAction(BaseAction):
    """
    Action to export GPS data to file.

    Handles validation, file dialog, and export process with
    appropriate user feedback.
    """

    def __init__(self,
                 data_controller: GPSDataProviderProtocol,
                 data_exporter: DataExporterProtocol,
                 parent_widget: Optional[QWidget] = None,
                 status_callback: Optional[StatusCallbackProtocol] = None):
        """
        Initialize export action.

        Args:
            data_controller: GPS data controller instance
            data_exporter: GPS data exporter instance
            parent_widget: Parent widget for dialogs
            status_callback: Callback for status messages (message, duration)
        """
        self.data_controller = data_controller
        self.data_exporter = data_exporter
        self.parent_widget = parent_widget
        self.status_callback = status_callback

    def can_execute(self) -> bool:
        """Check if export can be performed."""
        is_valid, _ = self.data_controller.validate_export_data()
        return is_valid

    def execute(self) -> None:
        """Execute the export action."""
        # Validate data availability
        is_valid, error_msg = self.data_controller.validate_export_data()
        if not is_valid:
            self._show_error("Export Error", error_msg)
            return

        # Get filename from user
        filename = self._get_export_filename()
        if not filename:
            return  # User cancelled

        # Perform export
        gps_data = self.data_controller.get_current_data()
        success, error_msg = self.data_exporter.export_to_file(gps_data, filename)

        if success:
            self._handle_export_success(filename)
        else:
            self._handle_export_failure(error_msg)

    def _get_export_filename(self) -> Optional[str]:
        """
        Show file dialog and get export filename.

        Returns:
            Filename or None if cancelled
        """
        default_filename = self.data_exporter.generate_default_filename()
        file_filter = self.data_exporter.get_file_filter()
        filename, _ = QFileDialog.getSaveFileName(
            self.parent_widget,
            "Export GPS Data",
            default_filename,
            file_filter
        )
        return filename if filename else None

    def _handle_export_success(self, filename: str) -> None:
        """Handle successful export."""
        basename = os.path.basename(filename)
        if self.status_callback:
            self.status_callback(f"GPS data exported to {basename}", 3000)

        QMessageBox.information(
            self.parent_widget,
            "Export Successful",
            f"GPS data successfully exported to:\n{filename}"
        )

    def _handle_export_failure(self, error_msg: str) -> None:
        """Handle export failure."""
        if self.status_callback:
            self.status_callback(f"Export failed: {error_msg}", 3000)

        self._show_error("Export Error", error_msg)

    def _show_error(self, title: str, message: str) -> None:
        """Show error dialog."""
        QMessageBox.warning(self.parent_widget, title, message)
