from PySide6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont

class Sidebar(QFrame):
    """
    Navigation sidebar for the main window.
    Emits a signal 'page_changed' with the target page index or name.
    """
    page_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("sidebar")
        self.setFixedWidth(220)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(10)

        # Title
        title = QLabel("CYBER\nTOOLKIT")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Consolas", 18, QFont.Bold))
        title.setStyleSheet("color: #00e676; margin-bottom: 20px;")
        layout.addWidget(title)

        # Navigation Buttons
        self.buttons = {
            "Dashboard": QPushButton("📊 Dashboard"),
            "Port Scanner": QPushButton("🔍 Port Scanner"),
            "Network Scanner": QPushButton("📡 Network Scanner"),
            "Password Analyzer": QPushButton("🔐 Password Analyzer"),
            "Connection Monitor": QPushButton("🌐 Conns Monitor"),
            "Firewall": QPushButton("🛡️ Firewall Sim"),
            "Scan History": QPushButton("📁 Scan History"),
            "Reports": QPushButton("🧾 Reports"),
            "Settings": QPushButton("⚙️ Settings")
        }

        for name, btn in self.buttons.items():
            btn.setCheckable(True)
            # lambda scoping fix using default arg
            btn.clicked.connect(lambda checked, n=name: self._on_button_clicked(n))
            
            # Styling specific to sidebar buttons to make them look like tabs
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding-left: 15px;
                    border: none;
                    background: transparent;
                    color: #a0a0a0;
                    font-size: 14px;
                }
                QPushButton:hover {
                    color: #00e676;
                    background-color: #1f2233;
                }
                QPushButton:checked {
                    color: #00e676;
                    background-color: #1f2233;
                    border-left: 3px solid #00e676;
                    border-radius: 0px;
                }
            """)
            layout.addWidget(btn)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.btn_logout = QPushButton("🚪 Logout")
        self.btn_logout.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding-left: 15px;
                border: none;
                background: transparent;
                color: #ff5555;
            }
            QPushButton:hover { background-color: #1f2233; }
        """)
        layout.addWidget(self.btn_logout)

        # Select first by default
        self.buttons["Dashboard"].setChecked(True)

    def _on_button_clicked(self, name):
        # Uncheck all others
        for n, btn in self.buttons.items():
            if n != name:
                btn.setChecked(False)
            else:
                btn.setChecked(True)
                
        self.page_changed.emit(name)
