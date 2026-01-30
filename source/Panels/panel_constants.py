"""
Shared constants for panel styling across the application.
This ensures a consistent appearance for all panels.
"""

# Text display constants
INVALID_VALUE_TEXT = "N/A"

# Panel dimensions
PANEL_WIDTH = 350
PANEL_HEIGHT = 126

# Font sizes
LABEL_FONT_SIZE = 15
TITLE_FONT_SIZE = 20

# Label heights
TITLE_HEIGHT = 30
KEY_LABEL_HEIGHT = 20
VALUE_LABEL_HEIGHT = 22

# Color scheme
PANEL_BACKGROUND_COLOR = "#f5f5f5"
PANEL_BORDER_COLOR = "#d0d0d0"
TITLE_BACKGROUND_COLOR = "#e8e8e8"
TEXT_COLOR = "#333333"
VALUE_COLOR = "#000000"

# Styling
PANEL_STYLE = f"""
    background-color: {PANEL_BACKGROUND_COLOR};
    border: 1px solid {PANEL_BORDER_COLOR};
    border-radius: 6px;
"""

TITLE_STYLE = f"""
    font-size: {TITLE_FONT_SIZE}px;
    font-weight: bold;
    color: {TEXT_COLOR};
    background-color: {TITLE_BACKGROUND_COLOR};
    border: none;
    border-bottom: 1px solid {PANEL_BORDER_COLOR};
    padding: 4px;
"""

KEY_LABEL_STYLE = f"""
    font-size: {LABEL_FONT_SIZE}px;
    color: {TEXT_COLOR};
    font-weight: 600;
    border: none;
    padding-right: 8px;
"""

VALUE_LABEL_STYLE = f"""
    font-size: {LABEL_FONT_SIZE}px;
    color: {VALUE_COLOR};
    border: none;
    padding-left: 4px;
"""
