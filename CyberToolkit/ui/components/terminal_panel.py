from PySide6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QLineEdit
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor, QTextCursor, QTextCharFormat

class TerminalPanel(QWidget):
    """
    A simulated terminal panel for issuing text commands.
    """
    command_issued = Signal(str, list) # command, args

    def __init__(self):
        super().__init__()
        self.setFixedHeight(200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.output_area = QPlainTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setFont(QFont("Consolas", 10))
        self.output_area.setStyleSheet("background-color: #000000; color: #00ff00; border: none; padding: 5px;")
        
        self.input_area = QLineEdit()
        self.input_area.setFont(QFont("Consolas", 10))
        self.input_area.setStyleSheet("background-color: #000000; color: #00ff00; border: none; border-top: 1px solid #005500; padding: 5px;")
        self.input_area.setPlaceholderText("root@cybertoolkit:~# (type 'help')")
        self.input_area.returnPressed.connect(self.handle_input)

        layout.addWidget(self.output_area)
        layout.addWidget(self.input_area)

        self.println("CyberToolkit Terminal Simulator v1.0 initialized.")
        self.println("Type 'help' for available commands.")

    def handle_input(self):
        text = self.input_area.text().strip()
        self.input_area.clear()
        
        if not text:
            return

        self.println(f"root@cybertoolkit:~# {text}", color="#ffffff")
        
        parts = text.split()
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == "clear":
            self.output_area.clear()
        elif cmd == "help":
            self.println("Available commands:", color="#00e676")
            self.println("  scan <port|network> - Initiate a scan")
            self.println("  history             - Show brief history log")
            self.println("  clear               - Clear terminal output")
            self.println("  help                - Show this message")
        else:
            # Emit to main window to handle
            self.command_issued.emit(cmd, args)

    def println(self, text, color="#00ff00"):
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        
        cursor = self.output_area.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text + "\\n", fmt)
        self.output_area.ensureCursorVisible()
