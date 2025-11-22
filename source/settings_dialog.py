import serial.tools.list_ports
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QGroupBox,
                             QLabel, QComboBox, QPushButton, QSlider)


class SettingsDialog(QDialog):
    def __init__(self, parent=None, current_port=None, current_baudrate=9600, update_interval=100,
                 reconnect_interval=5000):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.setMinimumWidth(400)

        self.current_port = current_port
        self.current_baudrate = current_baudrate
        self.update_interval = update_interval
        self.reconnect_interval = reconnect_interval

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Serial Port Configuration
        port_group = QGroupBox("Serial Port Configuration")
        port_layout = QVBoxLayout()

        # Port selection
        port_select_layout = QHBoxLayout()
        port_label = QLabel("Port:")
        self.port_combo = QComboBox()
        self.port_combo.setEditable(True)
        self.scan_ports()

        # Set current port if exists
        if self.current_port:
            index = self.port_combo.findText(self.current_port)
            if index >= 0:
                self.port_combo.setCurrentIndex(index)
            else:
                self.port_combo.setEditText(self.current_port)

        scan_button = QPushButton("Scan Ports")
        scan_button.clicked.connect(self.scan_ports)

        port_select_layout.addWidget(port_label)
        port_select_layout.addWidget(self.port_combo, 1)
        port_select_layout.addWidget(scan_button)

        # Baud rate selection
        baud_layout = QHBoxLayout()
        baud_label = QLabel("Baud Rate:")
        self.baud_combo = QComboBox()
        self.baud_combo.addItems(["4800", "9600", "19200", "38400", "57600", "115200"])
        self.baud_combo.setCurrentText(str(self.current_baudrate))

        baud_layout.addWidget(baud_label)
        baud_layout.addWidget(self.baud_combo)
        baud_layout.addStretch()

        port_layout.addLayout(port_select_layout)
        port_layout.addLayout(baud_layout)
        port_group.setLayout(port_layout)

        # Update Intervals
        interval_group = QGroupBox("Update Intervals")
        interval_layout = QVBoxLayout()

        # GPS Update interval
        gps_update_layout = QVBoxLayout()
        self.gps_update_label = QLabel(f"GPS Update: {self.update_interval}ms")
        self.gps_update_slider = QSlider(QtCore.Qt.Horizontal)
        self.gps_update_slider.setMinimum(50)
        self.gps_update_slider.setMaximum(1000)
        self.gps_update_slider.setValue(self.update_interval)
        self.gps_update_slider.setTickPosition(QSlider.TicksBelow)
        self.gps_update_slider.setTickInterval(100)
        self.gps_update_slider.valueChanged.connect(
            lambda v: self.gps_update_label.setText(f"GPS Update: {v}ms")
        )

        gps_update_layout.addWidget(self.gps_update_label)
        gps_update_layout.addWidget(self.gps_update_slider)

        # Reconnect interval
        reconnect_layout = QVBoxLayout()
        self.reconnect_label = QLabel(f"Reconnect Interval: {self.reconnect_interval}ms")
        self.reconnect_slider = QSlider(QtCore.Qt.Horizontal)
        self.reconnect_slider.setMinimum(1000)
        self.reconnect_slider.setMaximum(30000)
        self.reconnect_slider.setValue(self.reconnect_interval)
        self.reconnect_slider.setTickPosition(QSlider.TicksBelow)
        self.reconnect_slider.setTickInterval(5000)
        self.reconnect_slider.valueChanged.connect(
            lambda v: self.reconnect_label.setText(f"Reconnect Interval: {v}ms")
        )

        reconnect_layout.addWidget(self.reconnect_label)
        reconnect_layout.addWidget(self.reconnect_slider)

        interval_layout.addLayout(gps_update_layout)
        interval_layout.addLayout(reconnect_layout)
        interval_group.setLayout(interval_layout)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        # Add all to main layout
        main_layout.addWidget(port_group)
        main_layout.addWidget(interval_group)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def scan_ports(self):
        """Scan and populate available serial ports."""
        current_text = self.port_combo.currentText()
        self.port_combo.clear()

        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.port_combo.addItem(f"{port.device} - {port.description}", port.device)

        # Restore previous selection if still available
        if current_text:
            index = self.port_combo.findText(current_text, QtCore.Qt.MatchStartsWith)
            if index >= 0:
                self.port_combo.setCurrentIndex(index)

    def get_settings(self):
        """Return selected settings as dictionary."""
        # Extract just the device path if combo format is "device - description"
        port_text = self.port_combo.currentText()
        if ' - ' in port_text:
            port = port_text.split(' - ')[0]
        else:
            port = port_text

        return {
            'port': port,
            'baudrate': int(self.baud_combo.currentText()),
            'update_interval': self.gps_update_slider.value(),
            'reconnect_interval': self.reconnect_slider.value()
        }
