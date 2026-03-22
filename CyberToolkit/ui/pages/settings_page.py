from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                               QComboBox, QPushButton, QMessageBox)
from PySide6.QtGui import QFont

class SettingsPage(QWidget):
    def __init__(self, user_system):
        super().__init__()
        self.user_system = user_system
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        header = QLabel("Settings")
        header.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.setStyleSheet("color: #00e676;")
        layout.addWidget(header)
        
        # Theme Setting
        layout.addWidget(QLabel("Theme Strategy:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark Hacker", "Matrix", "Light Mode"])
        layout.addWidget(self.theme_combo)
        
        # Apply button
        btn_apply = QPushButton("Apply Visuals")
        btn_apply.clicked.connect(self.save_settings)
        layout.addWidget(btn_apply)
        
        layout.addStretch()

    def load_settings(self):
        user_data = self.user_system.get_user_data()
        settings = user_data.get("settings", {})
        
        theme = settings.get("theme", "Dark Hacker")
        idx = self.theme_combo.findText(theme)
        if idx >= 0:
            self.theme_combo.setCurrentIndex(idx)

    def save_settings(self):
        theme = self.theme_combo.currentText()
        self.user_system.update_settings({"theme": theme})
        
        # Request main window to update theme via its child/parent tree implicitly
        # (Alternatively fire a signal, but in our simplified model we'll prompt a restart warning)
        QMessageBox.information(self, "Settings Saved", "Visual preferences updated. Theme changes may require restarting the application or will apply to newly loaded components.")
