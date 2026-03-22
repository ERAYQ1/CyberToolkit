from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
                               QHeaderView, QProgressBar, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from modules.network_scanner import NetworkScannerWorker

class NetworkScannerPage(QWidget):
    def __init__(self, user_system):
        super().__init__()
        self.user_system = user_system
        self.worker = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        header = QLabel("Network Scanner (ARP)")
        header.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.setStyleSheet("color: #00e676;")
        layout.addWidget(header)
        
        input_layout = QHBoxLayout()
        
        self.ip_range_input = QLineEdit()
        self.ip_range_input.setPlaceholderText("IP Range (e.g., 192.168.1.1/24)")
        
        self.btn_scan = QPushButton("START SCAN")
        self.btn_scan.clicked.connect(self.start_scan)
        
        input_layout.addWidget(self.ip_range_input)
        input_layout.addWidget(self.btn_scan)
        
        layout.addLayout(input_layout)
        
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        layout.addWidget(self.progress)
        
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["IP Address", "MAC Address", "Vendor"])
        header_view = self.table.horizontalHeader()
        header_view.setSectionResizeMode(0, QHeaderView.Stretch)
        header_view.setSectionResizeMode(1, QHeaderView.Stretch)
        header_view.setSectionResizeMode(2, QHeaderView.Stretch)
        
        layout.addWidget(self.table)

    def start_scan(self):
        ip_range = self.ip_range_input.text().strip()
        if not ip_range:
            QMessageBox.warning(self, "Error", "Please enter an IP Range.")
            return

        reply = QMessageBox.question(self, "Security Warning", 
                                     f"Are you authorized to scan {ip_range}?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return

        self.table.setRowCount(0)
        self.btn_scan.setEnabled(False)
        self.progress.setValue(0)
        
        self.worker = NetworkScannerWorker(ip_range)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.device_found.connect(self.on_device_found)
        self.worker.finished.connect(self.on_scan_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_device_found(self, device):
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        ip_item = QTableWidgetItem(device.get("ip", ""))
        mac_item = QTableWidgetItem(device.get("mac", ""))
        vendor_item = QTableWidgetItem(device.get("vendor", ""))
        
        # Highlight logic could be placed here comparing against previous known devices
        ip_item.setForeground(Qt.green)
        
        self.table.setItem(row, 0, ip_item)
        self.table.setItem(row, 1, mac_item)
        self.table.setItem(row, 2, vendor_item)

    def on_scan_finished(self, devices):
        self.btn_scan.setEnabled(True)
        self.progress.setValue(100)
        self.user_system.save_scan_result("Network Scan", {"range": self.ip_range_input.text(), "devices": devices})
        
        # Reset progress bar after brief pause
        self.progress.setValue(0)

    def on_error(self, err_msg):
        self.btn_scan.setEnabled(True)
        QMessageBox.critical(self, "Error", err_msg)
