from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QProgressBar, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
from PySide6.QtCore import Qt
from modules.port_scanner import PortScanner
from utils.database import db
from .dashboard import create_info_box

class PortScannerPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Port Tarayıcı")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        layout.addWidget(create_info_box("Bu özellik nedir?", "Bir IP adresindeki bağlantı noktalarını (portları) taratarak hangilerinin açık olduğunu ve arkasında hangi servisin çalıştığını tahmin eder."))
        
        input_layout = QHBoxLayout()
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Hedef IP (örn. 127.0.0.1)")
        input_layout.addWidget(self.ip_input)
        
        self.start_port = QLineEdit()
        self.start_port.setPlaceholderText("Başlangıç Port (örn. 1)")
        self.start_port.setFixedWidth(130)
        input_layout.addWidget(self.start_port)
        
        self.end_port = QLineEdit()
        self.end_port.setPlaceholderText("Bitiş Port (örn. 1024)")
        self.end_port.setFixedWidth(130)
        input_layout.addWidget(self.end_port)
        
        self.btn_scan = QPushButton("Taramayı Başlat")
        self.btn_scan.clicked.connect(self.toggle_scan)
        input_layout.addWidget(self.btn_scan)
        layout.addLayout(input_layout)
        
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setTextVisible(True)
        layout.addWidget(self.progress)
        
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["IP Adresi", "Port", "Servis (Tahmin)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("background-color: #1e293b; color: #e2e8f0; gridline-color: #334155; border: 1px solid #334155;")
        self.table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #334155; color: white; border: 1px solid #475569; }")
        layout.addWidget(self.table)
        
        self.scanner = PortScanner()
        self.scanner.progress.connect(self.update_progress)
        self.scanner.result_found.connect(self.add_result)
        self.scanner.finished.connect(self.scan_finished)
        self.is_scanning = False
        self.found_ports = []

    def toggle_scan(self):
        if not self.is_scanning:
            ip = self.ip_input.text().strip()
            if not ip:
                QMessageBox.warning(self, "Hata", "Lütfen bir IP adresi girin.")
                return
            try:
                start = int(self.start_port.text().strip() or "1")
                end = int(self.end_port.text().strip() or "1024")
                if start > end or start < 1 or end > 65535: raise ValueError
            except ValueError:
                QMessageBox.warning(self, "Hata", "Geçersiz port aralığı. 1-65535 arası olmalı.")
                return
                
            reply = QMessageBox.question(self, "Uyarı", "Port taraması güvenlik alarmlarını tetikleyebilir. Devam edilsin mi?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No: return

            self.table.setRowCount(0)
            self.progress.setValue(0)
            self.btn_scan.setText("Taramayı Durdur")
            self.btn_scan.setStyleSheet("background-color: #ef4444; color: white;")
            self.is_scanning = True
            self.found_ports = []
            self.scanner.start_scan(ip, start, end)
        else:
            self.scanner.stop_scan()
            self.btn_scan.setText("Taramayı Başlat")
            self.btn_scan.setStyleSheet("")
            self.is_scanning = False

    def update_progress(self, val):
        self.progress.setValue(val)

    def add_result(self, ip, port, service):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(ip))
        self.table.setItem(row, 1, QTableWidgetItem(str(port)))
        self.table.setItem(row, 2, QTableWidgetItem(service))
        self.found_ports.append({"ip": ip, "port": port, "service": service})

    def scan_finished(self):
        self.progress.setValue(100)
        self.btn_scan.setText("Taramayı Başlat")
        self.btn_scan.setStyleSheet("")
        self.is_scanning = False
        db.add_history("Port S.", {"target": self.ip_input.text(), "open": len(self.found_ports)})
        QMessageBox.information(self, "Tamamlandı", f"Tarama bitti. {len(self.found_ports)} açık port bulundu.")
