from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QMessageBox
from PySide6.QtCore import Signal
from utils.database import db
from utils.translations import t, set_language
from .dashboard import create_info_box


class SettingsPage(QWidget):
    theme_changed = Signal(str)
    language_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(25, 25, 25, 25)
        self.layout.setSpacing(15)

        self.title = QLabel(t("settings_title"))
        self.title.setStyleSheet("font-size: 26px; font-weight: bold; color: #10b981;")
        self.layout.addWidget(self.title)

        # Theme selector
        theme_row = QHBoxLayout()
        self.theme_lbl = QLabel(t("theme_label"))
        self.theme_lbl.setStyleSheet("font-size: 14px;")
        theme_row.addWidget(self.theme_lbl)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark Hacker", "Matrix", "Light Mode"])
        current_theme = db.get_settings().get("theme", "Dark Hacker")
        idx = self.theme_combo.findText(current_theme)
        if idx >= 0:
            self.theme_combo.setCurrentIndex(idx)
        self.theme_combo.currentTextChanged.connect(self._on_theme_change)
        theme_row.addWidget(self.theme_combo)
        self.layout.addLayout(theme_row)

        # Language selector
        lang_row = QHBoxLayout()
        self.lang_lbl = QLabel(t("language_label"))
        self.lang_lbl.setStyleSheet("font-size: 14px;")
        lang_row.addWidget(self.lang_lbl)

        self.lang_combo = QComboBox()
        self.lang_combo.addItem("🇹🇷 Türkçe", "tr")
        self.lang_combo.addItem("🇬🇧 English", "en")
        self.lang_combo.addItem("🇩🇪 Deutsch", "de")

        current_lang = db.get_settings().get("language", "tr")
        lang_idx = self.lang_combo.findData(current_lang)
        if lang_idx >= 0:
            self.lang_combo.setCurrentIndex(lang_idx)
        self.lang_combo.currentIndexChanged.connect(self._on_lang_change)
        lang_row.addWidget(self.lang_combo)
        self.layout.addLayout(lang_row)

        # Clear data
        self.btn_clear = QPushButton(t("clear_data"))
        self.btn_clear.setStyleSheet("background-color: #ef4444; color: white; padding: 12px; font-weight: bold; border-radius: 6px; margin-top: 20px;")
        self.btn_clear.clicked.connect(self.clear_app_data)
        self.layout.addWidget(self.btn_clear)

        self.layout.addStretch()

    def _on_theme_change(self, text):
        db.update_settings({"theme": text})
        self.theme_changed.emit(text)

    def _on_lang_change(self, index):
        lang_code = self.lang_combo.itemData(index)
        db.update_settings({"language": lang_code})
        set_language(lang_code)
        self.language_changed.emit(lang_code)
        self.retranslate()
        QMessageBox.information(self, t("success"), t("lang_changed"))

    def retranslate(self):
        self.title.setText(t("settings_title"))
        self.theme_lbl.setText(t("theme_label"))
        self.lang_lbl.setText(t("language_label"))
        self.btn_clear.setText(t("clear_data"))

    def clear_app_data(self):
        reply = QMessageBox.question(self, t("warning"), t("clear_confirm"), QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            db.save({"users": {}, "history": [], "settings": {"theme": "Dark Hacker", "language": "tr"}})
            QMessageBox.information(self, t("success"), t("data_cleared"))
