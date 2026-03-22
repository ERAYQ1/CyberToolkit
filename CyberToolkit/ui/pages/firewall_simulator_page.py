from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QListWidget, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from modules.firewall_simulator import FirewallSimulator

class FirewallSimulatorPage(QWidget):
    def __init__(self):
        super().__init__()
        self.firewall = FirewallSimulator()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        header = QLabel("Firewall Simulator")
        header.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.setStyleSheet("color: #00e676;")
        layout.addWidget(header)
        
        layout.addWidget(QLabel("Simulate blocking specific IPs or Ports without affecting your actual system firewall."))
        
        # IP Blocks
        ip_layout = QHBoxLayout()
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Enter IP to block...")
        self.btn_block_ip = QPushButton("Block IP")
        self.btn_block_ip.clicked.connect(self.add_ip)
        
        ip_layout.addWidget(QLabel("IP Address:"))
        ip_layout.addWidget(self.ip_input)
        ip_layout.addWidget(self.btn_block_ip)
        layout.addLayout(ip_layout)
        
        self.ip_list = QListWidget()
        self.ip_list.itemDoubleClicked.connect(self.remove_ip)
        layout.addWidget(QLabel("Blocked IPs (Double click to remove):"))
        layout.addWidget(self.ip_list)
        
        # Port Blocks
        port_layout = QHBoxLayout()
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("Enter Port (e.g. 80)")
        self.btn_block_port = QPushButton("Block Port")
        self.btn_block_port.clicked.connect(self.add_port)
        
        port_layout.addWidget(QLabel("Port Number:"))
        port_layout.addWidget(self.port_input)
        port_layout.addWidget(self.btn_block_port)
        layout.addLayout(port_layout)
        
        self.port_list = QListWidget()
        self.port_list.itemDoubleClicked.connect(self.remove_port)
        layout.addWidget(QLabel("Blocked Ports (Double click to remove):"))
        layout.addWidget(self.port_list)
        
        self.refresh_lists()

    def refresh_lists(self):
        self.ip_list.clear()
        for ip in self.firewall.get_blocked_ips():
            self.ip_list.addItem(ip)
            
        self.port_list.clear()
        for port in self.firewall.get_blocked_ports():
            self.port_list.addItem(str(port))

    def add_ip(self):
        ip = self.ip_input.text().strip()
        if ip:
            if self.firewall.block_ip(ip):
                self.refresh_lists()
                self.ip_input.clear()
                QMessageBox.information(self, "Success", f"IP {ip} added to simulated block list.")

    def remove_ip(self, item):
        ip = item.text()
        if self.firewall.unblock_ip(ip):
            self.refresh_lists()

    def add_port(self):
        port_str = self.port_input.text().strip()
        if port_str.isdigit():
            port = int(port_str)
            if self.firewall.block_port(port):
                self.refresh_lists()
                self.port_input.clear()
                QMessageBox.information(self, "Success", f"Port {port} added to simulated block list.")
        else:
            QMessageBox.warning(self, "Error", "Port must be an integer.")

    def remove_port(self, item):
        port = int(item.text())
        if self.firewall.unblock_port(port):
            self.refresh_lists()
