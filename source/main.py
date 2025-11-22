import sys

from PyQt5.QtWidgets import QMessageBox

from application_factory import ApplicationFactory
from logging_config import configure_logging

configure_logging()

if __name__ == "__main__":
    try:
        factory = ApplicationFactory()
        factory.create_application(sys.argv)
        factory.create_main_window()
        factory.show()
        sys.exit(factory.exec())
    except Exception as e:
        QMessageBox.critical(None, "Startup Error", f"Failed to start application:\n{e}")
        sys.exit(1)
