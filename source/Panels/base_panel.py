from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QLabel

from Panels.panel_constants import TITLE_STYLE, TITLE_HEIGHT, KEY_LABEL_STYLE, KEY_LABEL_HEIGHT, VALUE_LABEL_STYLE, \
    VALUE_LABEL_HEIGHT, INVALID_VALUE_TEXT


class BasePanel(QWidget):
    def __init__(self):
        super().__init__()

    @staticmethod
    def create_title_label(title):
        label = QLabel(title)
        label.setStyleSheet(TITLE_STYLE)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setFixedHeight(TITLE_HEIGHT)
        return label

    def create_key_label(self, key):
        label = QLabel(key)
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setStyleSheet(KEY_LABEL_STYLE)
        label.setFixedHeight(KEY_LABEL_HEIGHT)
        return label

    def create_value_label(self, value):
        label = QLabel(value)
        label.setStyleSheet(VALUE_LABEL_STYLE)
        label.setFixedHeight(VALUE_LABEL_HEIGHT)
        label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        return label

    def _set_value_safe(self, label, value, format_spec, units, dir = ""):
        try:
            label.setText(f"{float(value):{format_spec}}{units} {dir}")
        except (ValueError, TypeError):
            label.setText(INVALID_VALUE_TEXT)
