"""
Application styling and theme configuration.
Centralizes all visual appearance settings for the GPS application.
"""
from dataclasses import dataclass

from PyQt5.QtGui import QFont, QPalette, QColor


@dataclass
class AppStyle:
    """
    Configuration for application appearance.

    Attributes:
        style_name: Qt style name (e.g., 'Fusion', 'Windows', 'Macintosh')
        app_name: Application name displayed in title bar
        app_version: Application version string
        font_family: Font family name
        font_size: Font size in points
        window_border: CSS border style for main window
        window_background_color: RGB tuple for window background (r, g, b)
    """
    style_name: str = 'macintosh'
    app_name: str = "GT-U7 GPS"
    app_version: str = "1.0"
    font_family: str = "Arial"
    font_size: int = 10
    window_border: str = "2px solid black"
    window_background_color: tuple = (255, 255, 255)  # White

    def get_font(self) -> QFont:
        """
        Create QFont from configuration.

        Returns:
            Configured QFont instance
        """
        return QFont(self.font_family, self.font_size)

    def get_palette(self) -> QPalette:
        """
        Create QPalette from configuration.

        Returns:
            Configured QPalette instance with window background color
        """
        palette = QPalette()
        r, g, b = self.window_background_color
        palette.setColor(QPalette.Window, QColor(r, g, b))
        return palette

    def get_window_stylesheet(self) -> str:
        """
        Get stylesheet for main window.

        Returns:
            CSS stylesheet string
        """
        return f"border: {self.window_border};"


# Default style configuration
DEFAULT_STYLE = AppStyle()

# Alternative style configurations
DARK_STYLE = AppStyle(
    style_name='Fusion',
    app_name="GT-U7 GPS",
    app_version="1.0",
    font_family="Arial",
    font_size=10,
    window_border="2px solid #333333",
    window_background_color=(45, 45, 45)  # Dark gray
)

MINIMAL_STYLE = AppStyle(
    style_name='Fusion',
    app_name="GT-U7 GPS",
    app_version="1.0",
    font_family="Arial",
    font_size=10,
    window_border="none",
    window_background_color=(255, 255, 255)
)
