from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout

from Panels.base_panel import BasePanel
from source.Panels.panel_constants import (
    INVALID_VALUE_TEXT, PANEL_WIDTH, PANEL_HEIGHT, PANEL_STYLE
)


class SatellitePanel(BasePanel):
    def __init__(self):
        super().__init__()
        grid_layout, self.num_sats, self.fix_quality = self.create_satellite_layout()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.create_title_label("Satellites"))
        main_layout.addLayout(grid_layout)
        main_layout.addStretch()
        main_layout.setSpacing(0)
        
        base_widget = self.create_base_widget()
        base_widget.setLayout(main_layout)

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(base_widget)
        self.setLayout(layout)

        # Set fixed size for alignment
        self.setFixedSize(PANEL_WIDTH, PANEL_HEIGHT)

    def create_base_widget(self) -> QWidget:
        base_widget = QWidget()
        base_widget.setStyleSheet(PANEL_STYLE)
        base_widget.setContentsMargins(0, 0, 0, 0)
        base_widget.setFixedWidth(PANEL_WIDTH)
        base_widget.setFixedHeight(PANEL_HEIGHT)
        return base_widget

    # private functions
    def create_satellite_layout(self):
        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        num_sats = self.create_value_label("0")
        fix_quality = self.create_value_label("None")

        fields = [("Count: ", num_sats), ("Fix Quality: ", fix_quality)]
        for row, (key, widget) in enumerate(fields):
            grid_layout.addWidget(self.create_key_label(key), row, 0)
            grid_layout.addWidget(widget, row, 1)

        return grid_layout, num_sats, fix_quality

    # public functions
    def set_num_sats(self, num_sats):
        try:
            self.num_sats.setText(str(int(num_sats)))
        except (ValueError, TypeError):
            self.num_sats.setText(INVALID_VALUE_TEXT)

    def set_fix_quality(self, quality):
        quality_map = {0: "Invalid", 1: "GPS", 2: "DGPS"}
        self.fix_quality.setText(quality_map.get(quality, "Unknown"))
