from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QLabel
import math

from Panels.panel_constants import TITLE_STYLE, TITLE_HEIGHT, KEY_LABEL_STYLE, KEY_LABEL_HEIGHT, VALUE_LABEL_STYLE, \
    VALUE_LABEL_HEIGHT, INVALID_VALUE_TEXT


def format_variable_precision(value: float, error: float) -> str:
    """
    Formats a value and its error consistently by:
    1. Rounding the error to one significant figure.
    2. Rounding the value to match the resulting decimal place of the error.
    """

    if error <= 0:
        # Handle zero or negative error gracefully (e.g., for exact counts)
        decimal_places = 2
    else:
        # Calculate the required number of decimal places (N)
        # E = floor(log10(error))
        # N = |E|
        exponent = math.floor(math.log10(error))
        decimal_places = abs(exponent)

    # --- 1. Rounding ---

    # Round the error to one significant figure (using N decimal places)
    # E.g., if error is 0.00832, N=3, rounded_error = 0.008
    rounded_error = round(error, decimal_places)

    # Round the main value to match the same N decimal places
    rounded_value = round(value, decimal_places)

    # --- 2. Formatting ---

    # Use f-strings to format to the calculated number of decimal places
    formatted_value = f"{rounded_value:.{decimal_places}f}"
    formatted_error = f"{rounded_error:.{decimal_places}f}"

    # Combine the results using the Unicode 'PLUS-MINUS SIGN' (±).
    return f"{formatted_value} \u00B1 {formatted_error}"


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

    def _set_value_safe(self, label, value, err, units, dir = ""):
        try:
            val = format_variable_precision(value, err)
            label.setText(f"({val}){units} {dir}")
        except (ValueError, TypeError):
            label.setText(INVALID_VALUE_TEXT)
