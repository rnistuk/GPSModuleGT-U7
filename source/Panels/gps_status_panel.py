from datetime import datetime

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout

from .base_panel import BasePanel
from .panel_constants import (
    PANEL_WIDTH, PANEL_HEIGHT, PANEL_STYLE, VALUE_LABEL_STYLE
)


class GPSStatusPanel(BasePanel):
    def __init__(self):
        super().__init__()
        grid_layout, self.connection_status, self.last_update = self.create_status_layout()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.create_title_label("GPS Status"))
        main_layout.addLayout(grid_layout)
        main_layout.addStretch()
        base_widget = QWidget()
        base_widget.setStyleSheet(PANEL_STYLE)
        base_widget.setContentsMargins(0, 0, 0, 0)
        base_widget.setFixedWidth(PANEL_WIDTH)
        base_widget.setFixedHeight(PANEL_HEIGHT)
        main_layout.setSpacing(0)
        base_widget.setLayout(main_layout)

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(base_widget)
        self.setLayout(layout)

        # Set fixed size for alignment
        self.setFixedSize(PANEL_WIDTH, PANEL_HEIGHT)

    # private functions
    def create_status_layout(self):
        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        connection_status = self.create_value_label("Disconnected")
        last_update = self.create_value_label("Never")

        fields = [("Connection: ", connection_status), ("Last Update: ", last_update)]
        for row, (key, widget) in enumerate(fields):
            grid_layout.addWidget(self.create_key_label(key), row, 0)
            grid_layout.addWidget(widget, row, 1)

        return grid_layout, connection_status, last_update

    # public functions
    def set_connection_status(self, connected):
        if connected:
            self.connection_status.setText("Connected")
            self.connection_status.setStyleSheet(VALUE_LABEL_STYLE + "color: #2ecc71; font-weight: bold;")
        else:
            self.connection_status.setText("Disconnected")
            self.connection_status.setStyleSheet(VALUE_LABEL_STYLE + "color: #e74c3c; font-weight: bold;")

    def update_timestamp(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.last_update.setText(now)
