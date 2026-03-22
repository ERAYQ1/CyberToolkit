import json
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel, QPushButton
from .dashboard import create_info_box
from utils.database import db

class ScanHistoryPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Tarama Geçmişi")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        layout.addWidget(create_info_box("Bu özellik nedir?", "Geçmişte yaptığınız veya arka planda sessizce yapılan tüm ağ olaylarını, port taramalarını sıralı olarak bir günlükte tutar."))
        
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: #1e293b;
                border: 1px solid #334155;
                font-family: monospace;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #334155;
            }
        """)
        layout.addWidget(self.list_widget)
        
        self.btn_refresh = QPushButton("Geçmişi Yenile")
        self.btn_refresh.clicked.connect(self.load_history)
        layout.addWidget(self.btn_refresh)
        
        self.load_history()

    def load_history(self):
        self.list_widget.clear()
        hist = db.get_history()
        for idx, entry in enumerate(reversed(hist)):
            t = entry.get("type", "Bilinmeyen Olay")
            details = entry.get("details", {})
            desc = f"[{t}] | {json.dumps(details)}"
            item = QListWidgetItem(desc)
            self.list_widget.addItem(item)
