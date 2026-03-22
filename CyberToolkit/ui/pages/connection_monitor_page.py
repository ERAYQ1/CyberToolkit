from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QTableWidget, QTableWidgetItem, QHeaderView, QPushButton)
from PySide6.QtGui import QFont, QColor

from modules.connection_monitor import ConnectionMonitorWorker

class ConnectionMonitorPage(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = ConnectionMonitorWorker(interval_sec=3)
        self.worker.connections_updated.connect(self.update_table)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        header_layout = QHBoxLayout()
        header = QLabel("Live Connection Monitor")
        header.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.setStyleSheet("color: #00e676;")
        
        self.btn_toggle = QPushButton("STOP MONITORING")
        self.btn_toggle.clicked.connect(self.toggle_monitor)
        
        header_layout.addWidget(header)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_toggle)
        
        layout.addLayout(header_layout)
        
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["Protocol", "Local Address", "Remote Address", "Status", "PID", "Suspicious"])
        header_view = self.table.horizontalHeader()
        header_view.setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.table)

    def toggle_monitor(self):
        if self.worker.is_running:
            self.worker.stop()
            self.btn_toggle.setText("START MONITORING")
            self.btn_toggle.setStyleSheet("background-color: #00e676; color: black;")
        else:
            self.worker.is_running = True
            self.worker.start()
            self.btn_toggle.setText("STOP MONITORING")
            self.btn_toggle.setStyleSheet("background-color: #1f2233; color: #00e676;")

    def update_table(self, conns):
        # We only want to update if it has changed, but for simplicity we rebuild the table
        self.table.setRowCount(0)
        self.table.setUpdatesEnabled(False)
        
        for c in conns:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            self.table.setItem(row, 0, QTableWidgetItem(f"{c['family']} {c['type']}"))
            self.table.setItem(row, 1, QTableWidgetItem(c['laddr']))
            self.table.setItem(row, 2, QTableWidgetItem(c['raddr']))
            self.table.setItem(row, 3, QTableWidgetItem(c['status']))
            self.table.setItem(row, 4, QTableWidgetItem(str(c['pid']) if c['pid'] else "N/A"))
            
            susp_text = "YES" if c['suspicious'] else "NO"
            susp_item = QTableWidgetItem(susp_text)
            if c['suspicious']:
                susp_item.setForeground(QColor("#ff5555"))
            
            self.table.setItem(row, 5, susp_item)
            
        self.table.setUpdatesEnabled(True)

    def start_worker(self):
        if not self.worker.isRunning():
            self.worker.start()

    def hideEvent(self, event):
        # Optional: gracefully pause worker when page isn't visible to save CPU
        # self.worker.stop()
        super().hideEvent(event)
        
    def showEvent(self, event):
        # Optional: resume
        if self.btn_toggle.text() == "STOP MONITORING":
            self.start_worker()
        super().showEvent(event)
