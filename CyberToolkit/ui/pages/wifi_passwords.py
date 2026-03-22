from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel,
                               QTableWidget, QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Qt
from modules.wifi_passwords import WiFiPasswords

class WiFiPasswordsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        title = QLabel("📶 Kayıtlı Wi-Fi Şifreleri")
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #3b82f6;")
        layout.addWidget(title)

        desc = QLabel("Bilgisayarınızın daha önce bağlandığı tüm Wi-Fi ağlarının adlarını ve kayıtlı şifrelerini gösterir. Unuttuğunuz şifreleri buradan kolayca bulabilirsiniz.")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #94a3b8; font-size: 13px;")
        layout.addWidget(desc)

        self.btn_scan = QPushButton("🔑 Kayıtlı Şifreleri Göster")
        self.btn_scan.setStyleSheet("""
            QPushButton { background-color: #3b82f6; color: white; font-size: 15px; font-weight: bold; padding: 12px; border-radius: 8px; border: none; }
            QPushButton:hover { background-color: #2563eb; }
        """)
        self.btn_scan.clicked.connect(self.load_passwords)
        layout.addWidget(self.btn_scan)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Ağ Adı (SSID)", "Şifre", "Güvenlik Türü"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("""
            QTableWidget { background-color: #0f172a; color: #e2e8f0; gridline-color: #334155; border: 1px solid #1e293b; border-radius: 8px; font-size: 13px; alternate-background-color: #1e293b; }
            QHeaderView::section { background-color: #1e293b; color: #94a3b8; border: none; padding: 8px; font-size: 13px; font-weight: bold; }
        """)
        layout.addWidget(self.table)

        self.wifi = WiFiPasswords()

    def load_passwords(self):
        self.table.setRowCount(0)
        profiles = self.wifi.get_profiles()
        for p in profiles:
            row = self.table.rowCount()
            self.table.insertRow(row)

            item_name = QTableWidgetItem(p["name"])
            item_name.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, item_name)

            item_pwd = QTableWidgetItem(p["password"])
            item_pwd.setTextAlignment(Qt.AlignCenter)
            if p["password"] and "yok" not in p["password"]:
                item_pwd.setForeground(Qt.green)
            self.table.setItem(row, 1, item_pwd)

            item_auth = QTableWidgetItem(p["auth"])
            item_auth.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, item_auth)
