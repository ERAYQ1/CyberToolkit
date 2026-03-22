from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel,
                               QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox)
from PySide6.QtCore import Qt
from modules.startup_manager import StartupManager

class StartupManagerPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        title = QLabel("🚀 Başlangıç Programları Yöneticisi")
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #f59e0b;")
        layout.addWidget(title)

        desc = QLabel("Bilgisayarınız açıldığında arka planda otomatik başlayan tüm programları listeler. İstemediğiniz programları devre dışı bırakarak bilgisayarınızın daha hızlı açılmasını sağlayabilirsiniz.")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #94a3b8; font-size: 13px;")
        layout.addWidget(desc)

        self.btn_scan = QPushButton("📋 Başlangıç Programlarını Listele")
        self.btn_scan.setStyleSheet("""
            QPushButton { background-color: #f59e0b; color: #0f172a; font-size: 15px; font-weight: bold; padding: 12px; border-radius: 8px; border: none; }
            QPushButton:hover { background-color: #d97706; }
        """)
        self.btn_scan.clicked.connect(self.load_items)
        layout.addWidget(self.btn_scan)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Program Adı", "Dosya Yolu", "Kaynak", "Durum"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("""
            QTableWidget { background-color: #0f172a; color: #e2e8f0; gridline-color: #334155; border: 1px solid #1e293b; border-radius: 8px; font-size: 13px; alternate-background-color: #1e293b; }
            QHeaderView::section { background-color: #1e293b; color: #94a3b8; border: none; padding: 8px; font-size: 13px; font-weight: bold; }
        """)
        layout.addWidget(self.table)

        self.btn_disable = QPushButton("❌ Seçili Programı Başlangıçtan Çıkar")
        self.btn_disable.setStyleSheet("background-color: #ef4444; color: white; padding: 10px; font-weight: bold; border-radius: 6px;")
        self.btn_disable.clicked.connect(self.disable_selected)
        layout.addWidget(self.btn_disable)

        self.manager = StartupManager()

    def load_items(self):
        self.table.setRowCount(0)
        items = self.manager.get_startup_items()
        for item in items:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(item["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(item["path"]))
            self.table.setItem(row, 2, QTableWidgetItem(item["source"]))
            self.table.setItem(row, 3, QTableWidgetItem(item["status"]))

    def disable_selected(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen tablodan bir program seçin.")
            return
        name = self.table.item(row, 0).text()
        source = self.table.item(row, 2).text()

        if "Registry" not in source:
            QMessageBox.information(self, "Bilgi", "Sadece Registry (Kullanıcı) tabanlı girişler devre dışı bırakılabilir.")
            return

        ans = QMessageBox.question(self, "Onay", f"'{name}' başlangıçtan kaldırılsın mı?")
        if ans == QMessageBox.Yes:
            success, msg = self.manager.disable_startup_item(name)
            QMessageBox.information(self, "Sonuç", msg)
            if success:
                self.load_items()
