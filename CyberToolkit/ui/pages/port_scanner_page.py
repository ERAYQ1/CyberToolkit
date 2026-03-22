from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
                               QHeaderView, QProgressBar, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from modules.port_scanner import PortScannerWorker

class PortScannerPage(QWidget):
    def __init__(self, user_system):
        super().__init__()
        self.user_system = user_system
        self.worker = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("Port Scanner")
        header.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.setStyleSheet("color: #00e676;")
        layout.addWidget(header)
        
        # Inputs Row
        input_layout = QHBoxLayout()
        
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Target IP (e.g., 127.0.0.1)")
        self.ip_input.setText("127.0.0.1")
        
        self.start_port = QLineEdit()
        self.start_port.setPlaceholderText("Start Port (1)")
        self.start_port.setText("1")
        
        self.end_port = QLineEdit()
        self.end_port.setPlaceholderText("End Port (1024)")
        self.end_port.setText("1024")
        
        self.btn_scan = QPushButton("START SCAN")
        self.btn_scan.clicked.connect(self.toggle_scan)
        
        input_layout.addWidget(self.ip_input, 2)
        input_layout.addWidget(self.start_port, 1)
        input_layout.addWidget(self.end_port, 1)
        input_layout.addWidget(self.btn_scan, 1)
        
        layout.addLayout(input_layout)
        
        # Progress Bar
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        layout.addWidget(self.progress)
        
        # Results Table
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Port", "Service", "Banner / Info"])
        header_view = self.table.horizontalHeader()
        header_view.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header_view.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header_view.setSectionResizeMode(2, QHeaderView.Stretch)
        
        layout.addWidget(self.table)

    def toggle_scan(self):
        if self.worker is not None and self.worker.isRunning():
            self.worker.stop()
            self.btn_scan.setText("START SCAN")
            self.btn_scan.setStyleSheet("")
            return
            
        ip = self.ip_input.text().strip()
        try:
            start = int(self.start_port.text())
            end = int(self.end_port.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Ports must be numbers.")
            return

        # Simple verification
        if not ip:
            QMessageBox.warning(self, "Error", "Please enter a Target IP.")
            return
            
        reply = QMessageBox.question(self, "Security Warning", 
                                     f"Are you authorized to scan {ip}?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return

        self.table.setRowCount(0)
        self.progress.setValue(0)
        self.btn_scan.setText("STOP SCAN")
        self.btn_scan.setStyleSheet("background-color: #ff5555; color: white;")
        
        self.worker = PortScannerWorker(ip, start, end)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.port_found.connect(self.on_port_found)
        self.worker.finished.connect(self.on_scan_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_port_found(self, port, service, banner):
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        port_item = QTableWidgetItem(str(port))
        port_item.setTextAlignment(Qt.AlignCenter)
        
        srv_item = QTableWidgetItem(service)
        srv_item.setTextAlignment(Qt.AlignCenter)
        
        bn_item = QTableWidgetItem(banner)
        
        self.table.setItem(row, 0, port_item)
        self.table.setItem(row, 1, srv_item)
        self.table.setItem(row, 2, bn_item)

    def on_scan_finished(self, result_dict):
        self.btn_scan.setText("START SCAN")
        self.btn_scan.setStyleSheet("")
        self.progress.setValue(100)
        self.user_system.save_scan_result("Port Scan", result_dict)
        QMessageBox.information(self, "Complete", f"Scan finished on {result_dict['target']}")

    def on_error(self, err_msg):
        self.btn_scan.setText("START SCAN")
        self.btn_scan.setStyleSheet("")
        QMessageBox.critical(self, "Error", err_msg)
