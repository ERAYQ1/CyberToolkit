from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt
from modules.network_scanner import NetworkScanner
from utils.database import db
from .dashboard import create_info_box

class NetworkScannerPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30) # Increased margins for cleaner look
        layout.setSpacing(20)
        
        title = QLabel("Tek Tıkla Ağ Tarayıcı")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #10b981;")
        layout.addWidget(title)
        
        layout.addWidget(create_info_box("Bu özellik nedir?", "Wi-Fi (veya kablolu) ağınıza kimlerin bağlı olduğunu anında bulur. Hiçbir ayar yapmanıza veya program indirmeniz gerekmez. Sadece büyük butona basın!"))
        
        self.btn_scan = QPushButton("🚀 Ağı Tarayıp Cihazları Bul")
        self.btn_scan.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 15px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        self.btn_scan.clicked.connect(self.toggle_scan)
        layout.addWidget(self.btn_scan)
        
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(10)
        self.progress.setStyleSheet("""
            QProgressBar {
                background-color: #1e293b;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: #10b981;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.progress)
        
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Bilgisayar/Verici IP", "Cihazın MAC Adresi", "Bilgi"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #0f172a; 
                color: #e2e8f0; 
                gridline-color: #334155; 
                border: 2px solid #1e293b;
                border-radius: 8px;
                font-size: 14px;
            }
            QHeaderView::section { 
                background-color: #1e293b; 
                color: #94a3b8; 
                border: none;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.table)
        
        self.scanner = NetworkScanner()
        self.scanner.progress.connect(self.update_progress)
        self.scanner.result_found.connect(self.add_result)
        self.scanner.finished.connect(self.scan_finished)
        self.is_scanning = False
        self.found_devices = []

    def toggle_scan(self):
        if not self.is_scanning:
            self.table.setRowCount(0)
            self.progress.setValue(0)
            
            self.btn_scan.setText("🛑 Taramayı Durdur")
            self.btn_scan.setStyleSheet("""
                QPushButton { background-color: #ef4444; color: white; font-size: 18px; font-weight: bold; padding: 15px; border-radius: 8px; border: none; }
                QPushButton:hover { background-color: #dc2626; }
            """)
            
            self.is_scanning = True
            self.found_devices = []
            
            # Auto scan directly
            self.scanner.start_scan()
        else:
            self.scanner.stop_scan()
            self.reset_button()
            self.is_scanning = False

    def reset_button(self):
        self.btn_scan.setText("🚀 Ağı Tarayıp Cihazları Bul")
        self.btn_scan.setStyleSheet("""
            QPushButton { background-color: #3b82f6; color: white; font-size: 18px; font-weight: bold; padding: 15px; border-radius: 8px; border: none; }
            QPushButton:hover { background-color: #2563eb; }
        """)

    def update_progress(self, val):
        self.progress.setValue(val)

    def add_result(self, ip, mac, vendor):
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
        
        # Vendor (Info)
        item_v = QTableWidgetItem(vendor)
        item_v.setTextAlignment(Qt.AlignCenter)
        if vendor == "Sizin Bilgisayarınız":
            item_v.setForeground(Qt.yellow)
        self.table.setItem(row, 2, item_v)
        
        self.found_devices.append({"ip": ip, "mac": mac, "vendor": vendor})

    def scan_finished(self):
        self.progress.setValue(100)
        self.reset_button()
        self.is_scanning = False
        db.add_history("Ağ T.", {"subnet": "Otomatik", "found": len(self.found_devices)})
