from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout
from Panels.base_panel import BasePanel
from source.Panels.panel_constants import (
    PANEL_WIDTH, PANEL_HEIGHT, PANEL_STYLE
)

class PositionPanel(BasePanel):
    def __init__(self, width : int = PANEL_WIDTH, height : int = PANEL_HEIGHT, style : str =PANEL_STYLE):
        super().__init__()
        grid_layout, self.latitude, self.longitude, self.height = self.create_position_layout()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.create_title_label("Position"))
        main_layout.addLayout(grid_layout)
        main_layout.addStretch()
        base_widget = QWidget()
        base_widget.setStyleSheet(style)
        base_widget.setContentsMargins(0, 0, 0, 0)
        base_widget.setFixedWidth(width)
        base_widget.setFixedHeight(height)
        main_layout.setSpacing(0)
        base_widget.setLayout(main_layout)

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(base_widget)
        self.setLayout(layout)

        # Set a fixed size for alignment
        self.setFixedSize(width, height)


    # private functions
    def create_position_layout(self):
        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        latitude_label = self.create_value_label("0.0")
        longitude_label = self.create_value_label("0.0")
        height_label = self.create_value_label("0.0")

        fields = [("Latitude: ", latitude_label), ("Longitude: ", longitude_label), ("Height: ", height_label)]
        for row, (key, widget) in enumerate(fields):
            grid_layout.addWidget(self.create_key_label(key), row, 0)
            grid_layout.addWidget(widget, row, 1)

        return grid_layout, latitude_label, longitude_label, height_label

    # public functions
    def set_latitude(self, latitude: float, lat_dir: str, lat_err:float = 1.0e-6) -> None:
        self._set_value_safe(self.latitude, latitude, lat_err, "°", lat_dir)

    def set_longitude(self, longitude: float, lon_dir: str, lon_err:float = 1.0e-6) -> None:
        self._set_value_safe(self.longitude, longitude, lon_err, "°", lon_dir)

    def set_height(self, height: float, height_err:float = 0.1) -> None:
        self._set_value_safe(self.height, height, height_err, " m")

    def set_position(self, latitude: float, lat_dir: str, longitude: float, lon_dir: str, height: float) -> None:
        self.set_latitude(latitude, lat_dir)
        self.set_longitude(longitude, lon_dir)
        self.set_height(height)

    def set_position(self, p):
        self.set_latitude(p['latitude'], p['lat_dir'], p['lat_err'])
        self.set_longitude(p['longitude'], p['lon_dir'], p['lon_err'])
        self.set_height(p['height'], p['height_err'])
