"""
Application factory for creating and configuring the GPS application.
Separates application setup concerns from the main entry point.
"""
from PyQt5.QtWidgets import QApplication, QStyleFactory

from app_config import AppConfig, DEFAULT_CONFIG
from app_style import AppStyle, DEFAULT_STYLE
from main_window import MainWindow

class ApplicationFactory:
    """
    Factory class for creating and configuring the GPS application.

    Handles application-level setup including style, fonts, and main window creation.
    """

    def __init__(self, style: AppStyle = None, config: AppConfig = None):
        """
        Initialize the application factory.

        Args:
            style: AppStyle configuration (uses DEFAULT_STYLE if not provided)
            config: AppConfig configuration (uses DEFAULT_CONFIG if not provided)
        """
        self.app = None
        self.window = None
        self.style = style or DEFAULT_STYLE
        self.config = config or DEFAULT_CONFIG

    def create_application(self, argv) -> QApplication:
        """
        Create and configure the QApplication instance.

        Args:
            argv: Command line arguments

        Returns:
            Configured QApplication instance
        """
        self.app = QApplication(argv)
        self._configure_application()
        return self.app

    def _configure_application(self):
        """Configure application-level settings."""
        self.app.setStyle(QStyleFactory.create(self.style.style_name))
        self.app.setApplicationName(self.style.app_name)
        self.app.setApplicationVersion(self.style.app_version)
        self.app.setFont(self.style.get_font())

    def create_main_window(self) -> MainWindow:
        """
        Create and configure the main window.

        Returns:
            Configured MainWindow instance
        """
        self.window = MainWindow(config=self.config)
        self._configure_window()
        return self.window

    def _configure_window(self):
        """Configure main window appearance."""
        self.window.setStyleSheet(self.style.get_window_stylesheet())
        self.window.setAutoFillBackground(True)
        self.window.setPalette(self.style.get_palette())

    def show(self):
        """Display the main window."""
        if self.window:
            self.window.show()

    def exec(self) -> int:
        """
        Start the application event loop.

        Returns:
            Application exit code
        """
        if self.app:
            return self.app.exec_()
        return 1
