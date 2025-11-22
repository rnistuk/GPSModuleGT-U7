"""
GPS Data Exporter for exporting GPS data to various formats.
Supports CSV export with extensibility for other formats.
"""
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from gps_data import GPSData

logger = logging.getLogger(__name__)


class DataExporter(ABC):
    """Abstract base class for GPS data exporters."""

    @abstractmethod
    def export(self, gps_data: GPSData, filename: str) -> bool:
        """
        Export GPS data to file.

        Args:
            gps_data: GPS data to export
            filename: Output filename

        Returns:
            True if export successful, False otherwise
        """
        pass

    @abstractmethod
    def get_file_extension(self) -> str:
        """Get the file extension for this exporter."""
        pass


class CSVExporter(DataExporter):
    """Export GPS data to CSV format."""

    def export(self, gps_data: GPSData, filename: str) -> bool:
        """
        Export GPS data to CSV file.

        Args:
            gps_data: GPS data to export
            filename: Output filename

        Returns:
            True if export successful, False otherwise
        """
        try:
            with open(filename, 'w') as f:
                # Write header
                f.write("Timestamp,Latitude,Longitude,Height (m),Satellites,GPS Quality\n")

                # Write GPS data
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                quality_map = {0: "Invalid", 1: "GPS", 2: "DGPS"}
                quality_str = quality_map.get(gps_data.gps_quality, "Unknown")

                f.write(f"{timestamp},{gps_data.latitude},{gps_data.longitude},"
                        f"{gps_data.height},{gps_data.num_sats},{quality_str}\n")

            logger.info(f"GPS data exported to {filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to export GPS data: {e}")
            return False

    def get_file_extension(self) -> str:
        """Get the file extension for CSV files."""
        return ".csv"


class GPSDataExporter:
    """
    High-level GPS data exporter that manages export operations.

    Provides convenience methods for exporting GPS data with automatic
    filename generation and format selection.
    """

    def __init__(self, exporter: DataExporter = None):
        """
        Initialize GPS data exporter.

        Args:
            exporter: DataExporter implementation (defaults to CSVExporter)
        """
        self.exporter = exporter or CSVExporter()

    def export_to_file(self, gps_data: GPSData, filename: str) -> tuple[bool, Optional[str]]:
        """
        Export GPS data to specified file.

        Args:
            gps_data: GPS data to export
            filename: Output filename

        Returns:
            Tuple of (success: bool, error_message: Optional[str])
        """
        if not gps_data.has_position():
            return False, "No GPS position data available to export"

        try:
            success = self.exporter.export(gps_data, filename)
            if success:
                return True, None
            else:
                return False, "Export failed (see logs for details)"
        except Exception as e:
            error_msg = f"Failed to export data: {e}"
            logger.error(error_msg)
            return False, error_msg

    def generate_default_filename(self) -> str:
        """
        Generate default filename with timestamp.

        Returns:
            Default filename string
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        extension = self.exporter.get_file_extension()
        return f"gps_data_{timestamp}{extension}"

    def get_file_filter(self) -> str:
        """
        Get file filter string for file dialogs.

        Returns:
            File filter string (e.g., "CSV Files (*.csv);;All Files (*)")
        """
        ext = self.exporter.get_file_extension()
        ext_upper = ext.upper().replace('.', '')
        return f"{ext_upper} Files (*{ext});;All Files (*)"
