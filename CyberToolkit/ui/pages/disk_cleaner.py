from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                               QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QFrame)
from PySide6.QtCore import Qt
from modules.disk_cleaner import DiskCleaner

class DiskCleanerPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        title = QLabel("🧹 Disk Temizleyici")
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #10b981;")
        layout.addWidget(title)

        desc = QLabel("Windows'un geçici dosyalar, önbellek ve internet kalıntıları ile zamanla şişen depolama alanını tarar ve tek tıkla temizler.")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #94a3b8; font-size: 13px;")
        layout.addWidget(desc)

        # Total stat card
        stat_row = QHBoxLayout()
        self.card_total = self._make_card("Toplam Çöp", "— MB", "#ef4444")
        self.card_files = self._make_card("Dosya Sayısı", "—", "#f59e0b")
        stat_row.addWidget(self.card_total)
        stat_row.addWidget(self.card_files)
        layout.addLayout(stat_row)

        self.btn_scan = QPushButton("🔍 Çöp Dosyaları Tara")
        self.btn_scan.setStyleSheet("""
            QPushButton { background-color: #3b82f6; color: white; font-size: 15px; font-weight: bold; padding: 12px; border-radius: 8px; border: none; }
            QPushButton:hover { background-color: #2563eb; }
        """)
        self.btn_scan.clicked.connect(self.scan_disk)
        layout.addWidget(self.btn_scan)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Klasör", "Konum", "Boyut (MB)", "Dosya Sayısı"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("""
            QTableWidget { background-color: #0f172a; color: #e2e8f0; gridline-color: #334155; border: 1px solid #1e293b; border-radius: 8px; font-size: 13px; alternate-background-color: #1e293b; }
            QHeaderView::section { background-color: #1e293b; color: #94a3b8; border: none; padding: 8px; font-size: 13px; font-weight: bold; }
        """)
        layout.addWidget(self.table)

        self.btn_clean = QPushButton("🗑️ Seçili Klasörü Temizle")
        self.btn_clean.setStyleSheet("background-color: #ef4444; color: white; padding: 10px; font-weight: bold; border-radius: 6px;")
        self.btn_clean.clicked.connect(self.clean_selected)
        layout.addWidget(self.btn_clean)

        self.cleaner = DiskCleaner()
        self._scan_data = []

    def _make_card(self, label, value, color):
        card = QFrame()
        card.setStyleSheet(f"QFrame {{ background-color: #1e293b; border-radius: 10px; border-left: 4px solid {color}; }}")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(14, 10, 14, 10)
        cl.setSpacing(4)
        lbl = QLabel(label)
        lbl.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold;")
        cl.addWidget(lbl)
        val = QLabel(value)
        val.setObjectName("value")
        val.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: bold;")
        cl.addWidget(val)
        return card

    def _update_card(self, card, text):
        lbl = card.findChild(QLabel, "value")
        if lbl:
            lbl.setText(text)

    def scan_disk(self):
        self.table.setRowCount(0)
        results, total_mb = self.cleaner.scan()
        self._scan_data = results

        total_files = 0
        for r in results:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(r["label"]))
            self.table.setItem(row, 1, QTableWidgetItem(r["path"]))

            item_size = QTableWidgetItem(f"{r['size_mb']} MB")
            item_size.setTextAlignment(Qt.AlignCenter)
            if r["size_mb"] > 100:
                item_size.setForeground(Qt.red)
            self.table.setItem(row, 2, item_size)

            item_count = QTableWidgetItem(str(r["files"]))
            item_count.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 3, item_count)
            total_files += r["files"]

        self._update_card(self.card_total, f"{total_mb} MB")
        self._update_card(self.card_files, str(total_files))

    def clean_selected(self):
        row = self.table.currentRow()
        if row < 0 or row >= len(self._scan_data):
            QMessageBox.warning(self, "Uyarı", "Lütfen tablodan bir klasör seçin.")
            return

        path = self._scan_data[row]["path"]
        label = self._scan_data[row]["label"]

        ans = QMessageBox.question(self, "Onay", f"'{label}' klasöründeki geçici dosyalar silinsin mi?")
        if ans == QMessageBox.Yes:
            deleted, errors = self.cleaner.clean(path)
            QMessageBox.information(self, "Temizlik Tamamlandı", f"{deleted} dosya silindi, {errors} dosya atlandi.")
            self.scan_disk()
