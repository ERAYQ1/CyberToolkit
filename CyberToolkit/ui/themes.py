DARK_HACKER = """
QWidget {
    background-color: #0f172a;
    color: #f1f5f9;
    font-family: 'Segoe UI', 'San Francisco', sans-serif;
    font-size: 14px;
}

QPushButton {
    background-color: #1e293b;
    border: 1px solid #3b82f6;
    border-radius: 6px;
    padding: 10px 16px;
    color: #60a5fa;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #3b82f6;
    color: #ffffff;
}

QPushButton:pressed {
    background-color: #2563eb;
}

QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 12px;
    color: #f8fafc;
    font-size: 14px;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #3b82f6;
    background-color: #0f172a;
}

QLabel {
    color: #cbd5e1;
}

QProgressBar {
    border: none;
    border-radius: 5px;
    text-align: center;
    color: transparent;
    background-color: #1e293b;
}

QProgressBar::chunk {
    background-color: #10b981;
    border-radius: 5px;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: #0f172a;
    width: 6px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #475569;
    min-height: 20px;
    border-radius: 3px;
}
QScrollBar::handle:vertical:hover {
    background: #64748b;
}

/* Base ComboBox for Settings */
QComboBox {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 8px;
    color: #f8fafc;
}
"""

MATRIX = """
QWidget {
    background-color: #000000;
    color: #00ff00;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 15px;
}

QPushButton {
    background-color: #001100;
    border: 1px solid #00ff00;
    border-radius: 0px;
    padding: 10px 16px;
    color: #00ff00;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #00ff00;
    color: #000000;
}

QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #001100;
    border: 1px dotted #00ff00;
    padding: 12px;
    color: #00ff00;
}

QProgressBar {
    border: 1px solid #00ff00;
    background-color: #000000;
}

QProgressBar::chunk {
    background-color: #00ff00;
}
"""

LIGHT_MODE = """
QWidget {
    background-color: #f8fafc;
    color: #0f172a;
    font-family: 'Segoe UI', 'San Francisco', sans-serif;
    font-size: 14px;
}

QPushButton {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 10px 16px;
    color: #2563eb;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #eff6ff;
    border-color: #93c5fd;
}

QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 12px;
    color: #0f172a;
}
"""

THEMES = {
    "Dark Hacker": DARK_HACKER,
    "Matrix": MATRIX,
    "Light Mode": LIGHT_MODE
}

def get_theme(name):
    return THEMES.get(name, DARK_HACKER)
