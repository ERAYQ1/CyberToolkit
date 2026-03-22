from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QProgressBar, QTableWidget, QTableWidgetItem,
                               QHeaderView, QMessageBox, QFrame)
from PySide6.QtCore import Qt
from modules.port_scanner import PortScanner
from utils.database import db
from .dashboard import create_info_box

class PortScannerPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        title = QLabel("🔍 Açık Port (Kapı) Tarayıcı")
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #f59e0b;")
        layout.addWidget(title)

        desc = QLabel("Bir IP adresindeki bağlantı kapılarını (port) tarar. Hangi kapıların açık olduğunu ve arkasında hangi servisin çalıştığını gösterir.")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #94a3b8; font-size: 13px;")
        layout.addWidget(desc)

        # Stat cards
        stats_row = QHBoxLayout()
        stats_row.setSpacing(12)
        self.card_target = self._make_stat("Hedef IP", "—", "#3b82f6")
        self.card_range = self._make_stat("Port Aralığı", "—", "#8b5cf6")
        self.card_open = self._make_stat("Açık Port", "0", "#ef4444")
        self.card_status = self._make_stat("Durum", "Bekliyor", "#10b981")
        stats_row.addWidget(self.card_target)
        stats_row.addWidget(self.card_range)
        stats_row.addWidget(self.card_open)
        stats_row.addWidget(self.card_status)
        layout.addLayout(stats_row)

        # Input Row
        input_layout = QHBoxLayout()
        input_layout.setSpacing(8)

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Hedef IP (örn. 192.168.1.1)")
        self.ip_input.setStyleSheet("padding: 10px; font-size: 14px; border-radius: 6px; border: 1px solid #334155; background-color: #1e293b; color: white;")
        input_layout.addWidget(self.ip_input)

        self.start_port = QLineEdit()
        self.start_port.setPlaceholderText("Başlangıç (1)")
        self.start_port.setFixedWidth(110)
        self.start_port.setStyleSheet("padding: 10px; font-size: 14px; border-radius: 6px; border: 1px solid #334155; background-color: #1e293b; color: white;")
        input_layout.addWidget(self.start_port)

        self.end_port = QLineEdit()
        self.end_port.setPlaceholderText("Bitiş (1024)")
        self.end_port.setFixedWidth(110)
        self.end_port.setStyleSheet("padding: 10px; font-size: 14px; border-radius: 6px; border: 1px solid #334155; background-color: #1e293b; color: white;")
        input_layout.addWidget(self.end_port)

        self.btn_scan = QPushButton("🚀 Taramayı Başlat")
        self.btn_scan.setStyleSheet("""
            QPushButton { background-color: #3b82f6; color: white; font-size: 14px; font-weight: bold; padding: 10px 20px; border-radius: 6px; border: none; }
            QPushButton:hover { background-color: #2563eb; }
        """)
        self.btn_scan.clicked.connect(self.toggle_scan)
        input_layout.addWidget(self.btn_scan)
        layout.addLayout(input_layout)

        # Progress
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(8)
        self.progress.setStyleSheet("""
            QProgressBar { background-color: #1e293b; border-radius: 4px; }
            QProgressBar::chunk { background-color: #f59e0b; border-radius: 4px; }
        """)
        layout.addWidget(self.progress)

        # Results Table
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["IP Adresi", "Port Numarası", "Servis (Tahmin)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #0f172a; color: #e2e8f0;
                gridline-color: #334155; border: 1px solid #1e293b;
                border-radius: 8px; font-size: 13px;
                alternate-background-color: #1e293b;
            }
            QHeaderView::section {
                background-color: #1e293b; color: #94a3b8;
                border: none; padding: 8px; font-size: 13px; font-weight: bold;
            }
        """)
        layout.addWidget(self.table)

        self.scanner = PortScanner()
        self.scanner.progress.connect(self.update_progress)
        self.scanner.result_found.connect(self.add_result)
        self.scanner.finished.connect(self.scan_finished)
        self.is_scanning = False
        self.found_ports = []

    def _make_stat(self, label, value, color):
        card = QFrame()
        card.setStyleSheet(f"QFrame {{ background-color: #1e293b; border-radius: 10px; border-left: 4px solid {color}; }}")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(12, 8, 12, 8)
        cl.setSpacing(2)
        lbl = QLabel(label)
        lbl.setStyleSheet("color: #94a3b8; font-size: 10px; font-weight: bold;")
        cl.addWidget(lbl)
        val = QLabel(value)
        val.setObjectName("value")
        val.setStyleSheet(f"color: {color}; font-size: 20px; font-weight: bold;")
        cl.addWidget(val)
        return card

    def _update_stat(self, card, text):
        lbl = card.findChild(QLabel, "value")
        if lbl:
            lbl.setText(text)

    def toggle_scan(self):
        if not self.is_scanning:
            ip = self.ip_input.text().strip()
            if not ip:
                QMessageBox.warning(self, "Hata", "Lütfen bir IP adresi girin.")
                return
            try:
                start = int(self.start_port.text().strip() or "1")
                end = int(self.end_port.text().strip() or "1024")
                if start > end or start < 1 or end > 65535:
                    raise ValueError
            except ValueError:
                QMessageBox.warning(self, "Hata", "Geçersiz port aralığı (1-65535).")
                return

            self.table.setRowCount(0)
            self.progress.setValue(0)
            self.found_ports = []

            self._update_stat(self.card_target, ip)
            self._update_stat(self.card_range, f"{start}-{end}")
            self._update_stat(self.card_open, "0")
            self._update_stat(self.card_status, "Tarıyor...")

            self.btn_scan.setText("🛑 Durdur")
            self.btn_scan.setStyleSheet("""
                QPushButton { background-color: #ef4444; color: white; font-size: 14px; font-weight: bold; padding: 10px 20px; border-radius: 6px; border: none; }
                QPushButton:hover { background-color: #dc2626; }
            """)
            self.is_scanning = True
            self.scanner.start_scan(ip, start, end)
        else:
            self.scanner.stop_scan()
            self._reset()
            self._update_stat(self.card_status, "Durduruldu")

    def _reset(self):
        self.btn_scan.setText("🚀 Taramayı Başlat")
        self.btn_scan.setStyleSheet("""
            QPushButton { background-color: #3b82f6; color: white; font-size: 14px; font-weight: bold; padding: 10px 20px; border-radius: 6px; border: none; }
            QPushButton:hover { background-color: #2563eb; }
        """)
        self.is_scanning = False

    def update_progress(self, val):
        self.progress.setValue(val)

    def add_result(self, ip, port, service):
        row = self.table.rowCount()
        self.table.insertRow(row)

        item_ip = QTableWidgetItem(ip)
        item_ip.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, 0, item_ip)

        item_port = QTableWidgetItem(str(port))
        item_port.setTextAlignment(Qt.AlignCenter)
        item_port.setForeground(Qt.red)
        self.table.setItem(row, 1, item_port)

        item_svc = QTableWidgetItem(service)
        item_svc.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, 2, item_svc)

        self.found_ports.append({"ip": ip, "port": port, "service": service})
        self._update_stat(self.card_open, str(len(self.found_ports)))

    def scan_finished(self):
        self.progress.setValue(100)
        self._reset()
        self._update_stat(self.card_status, "Tamamlandı")
        db.add_history("Port Scan", {"target": self.ip_input.text(), "open_ports_count": len(self.found_ports)})
