from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QMessageBox
from PySide6.QtCore import Signal
from utils.database import db
from .dashboard import create_info_box

class SettingsPage(QWidget):
    theme_changed = Signal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Uygulama Ayarları")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        layout.addWidget(create_info_box("Bu özellik nedir?", "Uygulamanın genel temasını değiştirebilir veya kaydedilmiş olan eski tarama geçmişlerini tamamen silebilirsiniz."))
        
        form_layout = QHBoxLayout()
        theme_lbl = QLabel("Arayüz Teması:")
        form_layout.addWidget(theme_lbl)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark Hacker", "Matrix", "Light Mode"])
        
        current_theme = db.get_settings().get("theme", "Dark Hacker")
        idx = self.theme_combo.findText(current_theme)
        if idx >= 0:
            self.theme_combo.setCurrentIndex(idx)
            
        self.theme_combo.currentTextChanged.connect(self._on_theme_change)
        form_layout.addWidget(self.theme_combo)
        layout.addLayout(form_layout)
        
        self.btn_clear_data = QPushButton("Tüm Uygulama Geçmişini Temizle")
        self.btn_clear_data.setStyleSheet("background-color: #ef4444; color: white; padding: 10px; margin-top: 30px;")
        self.btn_clear_data.clicked.connect(self.clear_app_data)
        layout.addWidget(self.btn_clear_data)
        
        layout.addStretch()

    def _on_theme_change(self, text):
        db.update_settings({"theme": text})
        self.theme_changed.emit(text)
        QMessageBox.information(self, "Tema Değişti", f"Tema '{text}' olarak güncellendi. Bazı kısımların tam ayarlanması için yeniden başlatma gerekebilir.")

    def clear_app_data(self):
        reply = QMessageBox.question(self, "Dikkat", "Bu işlem tüm kayıtlı tarama geçmişini ve ayarları SİLECEKTİR. Devam edilsin mi?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            db.save({"users": {}, "history": [], "settings": {"theme": "Dark Hacker"}})
            QMessageBox.information(self, "Başarılı", "Tüm uygulama verileri temizlendi.")
