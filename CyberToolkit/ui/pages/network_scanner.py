from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QProgressBar, QTableWidget,
                               QTableWidgetItem, QHeaderView, QFrame)
from PySide6.QtCore import Qt
from modules.network_scanner import NetworkScanner
from utils.database import db

class NetworkScannerPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # Title
        title = QLabel("🌐 Ağ Tarayıcı")
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #10b981;")
        layout.addWidget(title)

        desc = QLabel("Wi-Fi veya kablolu ağınıza bağlı tüm cihazları (telefon, TV, yazıcı, bilgisayar vb.) otomatik olarak tespit eder. Cihaz türünü, IP/MAC adresini, yanıt süresini ve makine ismini gösterir.")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #94a3b8; font-size: 13px; margin-bottom: 5px;")
        layout.addWidget(desc)

        # Stats Cards Row
        stats_row = QHBoxLayout()
        stats_row.setSpacing(12)

        self.card_total = self._make_stat_card("Bulunan Cihaz", "0", "#3b82f6")
        self.card_router = self._make_stat_card("Modem / Router", "—", "#f59e0b")
        self.card_fastest = self._make_stat_card("En Hızlı Yanıt", "— ms", "#10b981")
        self.card_slowest = self._make_stat_card("En Yavaş Yanıt", "— ms", "#ef4444")

        stats_row.addWidget(self.card_total)
        stats_row.addWidget(self.card_router)
        stats_row.addWidget(self.card_fastest)
        stats_row.addWidget(self.card_slowest)
        layout.addLayout(stats_row)

        # Scan Button
        self.btn_scan = QPushButton("🚀 Ağı Tarayıp Cihazları Bul")
        self.btn_scan.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6; color: white; font-size: 16px;
                font-weight: bold; padding: 14px; border-radius: 8px; border: none;
            }
            QPushButton:hover { background-color: #2563eb; }
        """)
        self.btn_scan.clicked.connect(self.toggle_scan)
        layout.addWidget(self.btn_scan)

        # Progress
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(8)
        self.progress.setStyleSheet("""
            QProgressBar { background-color: #1e293b; border-radius: 4px; }
            QProgressBar::chunk { background-color: #10b981; border-radius: 4px; }
        """)
        layout.addWidget(self.progress)

        self.lbl_status = QLabel("")
        self.lbl_status.setAlignment(Qt.AlignCenter)
        self.lbl_status.setStyleSheet("color: #64748b; font-size: 12px;")
        layout.addWidget(self.lbl_status)

        # Results Table (6 columns)
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "IP Adresi", "MAC Adresi", "Cihaz Türü", "Makine Adı", "Yanıt (ms)", "Durum"
        ])
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

        # Scanner backend
        self.scanner = NetworkScanner()
        self.scanner.progress.connect(self.update_progress)
        self.scanner.result_found.connect(self.add_result)
        self.scanner.finished.connect(self.scan_finished)
        self.is_scanning = False
        self.found_devices = []
        self._fastest = 9999.0
        self._slowest = 0.0
        self._router_ip = ""

    def _make_stat_card(self, label, value, color):
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #1e293b; border-radius: 10px;
                border-left: 4px solid {color}; padding: 10px;
            }}
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(12, 10, 12, 10)
        card_layout.setSpacing(4)

        lbl = QLabel(label)
        lbl.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold;")
        card_layout.addWidget(lbl)

        val = QLabel(value)
        val.setObjectName("value")
        val.setStyleSheet(f"color: {color}; font-size: 22px; font-weight: bold;")
        card_layout.addWidget(val)

        return card

    def _update_card_value(self, card, text):
        lbl = card.findChild(QLabel, "value")
        if lbl:
            lbl.setText(text)

    def toggle_scan(self):
        if not self.is_scanning:
            self.table.setRowCount(0)
            self.progress.setValue(0)
            self.found_devices = []
            self._fastest = 9999.0
            self._slowest = 0.0
            self._router_ip = ""
            self._update_card_value(self.card_total, "0")
            self._update_card_value(self.card_router, "—")
            self._update_card_value(self.card_fastest, "— ms")
            self._update_card_value(self.card_slowest, "— ms")

            self.btn_scan.setText("🛑 Taramayı Durdur")
            self.btn_scan.setStyleSheet("""
                QPushButton { background-color: #ef4444; color: white; font-size: 16px; font-weight: bold; padding: 14px; border-radius: 8px; border: none; }
                QPushButton:hover { background-color: #dc2626; }
            """)
            self.lbl_status.setText("Ağ taranıyor, lütfen bekleyin...")

            self.is_scanning = True
            self.scanner.start_scan()
        else:
            self.scanner.stop_scan()
            self.reset_button()
            self.is_scanning = False
            self.lbl_status.setText("Tarama kullanıcı tarafından durduruldu.")

    def reset_button(self):
        self.btn_scan.setText("🚀 Ağı Tarayıp Cihazları Bul")
        self.btn_scan.setStyleSheet("""
            QPushButton { background-color: #3b82f6; color: white; font-size: 16px; font-weight: bold; padding: 14px; border-radius: 8px; border: none; }
            QPushButton:hover { background-color: #2563eb; }
        """)

    def update_progress(self, val):
        self.progress.setValue(val)

    def add_result(self, ip, mac, device_type, hostname, response_ms):
        row = self.table.rowCount()
        self.table.insertRow(row)

        # IP
        item_ip = QTableWidgetItem(ip)
        item_ip.setForeground(Qt.green)
        item_ip.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, 0, item_ip)

        # MAC
        item_mac = QTableWidgetItem(mac)
        item_mac.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, 1, item_mac)

        # Device Type
        item_type = QTableWidgetItem(device_type)
        item_type.setTextAlignment(Qt.AlignCenter)
        if "Bu Bilgisayar" in device_type:
            item_type.setForeground(Qt.yellow)
        elif "Modem" in device_type:
            item_type.setForeground(Qt.cyan)
            self._router_ip = ip
            self._update_card_value(self.card_router, ip)
        self.table.setItem(row, 2, item_type)

        # Hostname
        item_host = QTableWidgetItem(hostname if hostname else "—")
        item_host.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, 3, item_host)

        # Response Time
        if response_ms >= 0:
            item_resp = QTableWidgetItem(f"{response_ms} ms")
            if response_ms < self._fastest:
                self._fastest = response_ms
                self._update_card_value(self.card_fastest, f"{response_ms} ms")
            if response_ms > self._slowest:
                self._slowest = response_ms
                self._update_card_value(self.card_slowest, f"{response_ms} ms")
        else:
            item_resp = QTableWidgetItem("Zaman aşımı")
        item_resp.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, 4, item_resp)

        # Status
        item_status = QTableWidgetItem("🟢 Çevrimiçi")
        item_status.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, 5, item_status)

        self.found_devices.append({"ip": ip, "mac": mac, "type": device_type})
        self._update_card_value(self.card_total, str(len(self.found_devices)))

    def scan_finished(self, total):
        self.progress.setValue(100)
        self.reset_button()
        self.is_scanning = False
        self.lbl_status.setText(f"Tarama tamamlandı. Toplam {len(self.found_devices)} cihaz bulundu.")
        db.add_history("Network Scan", {"subnet": "Auto /24", "devices_found": len(self.found_devices)})
