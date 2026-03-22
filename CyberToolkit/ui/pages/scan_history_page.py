from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                               QTreeWidget, QTreeWidgetItem, QPushButton, QHBoxLayout)
from PySide6.QtGui import QFont

class ScanHistoryPage(QWidget):
    def __init__(self, user_system):
        super().__init__()
        self.user_system = user_system
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header Area
        header_layout = QHBoxLayout()
        header = QLabel("Scan History")
        header.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.setStyleSheet("color: #00e676;")
        
        btn_refresh = QPushButton("REFRESH HISTORY")
        btn_refresh.clicked.connect(self.load_history)
        
        header_layout.addWidget(header)
        header_layout.addStretch()
        header_layout.addWidget(btn_refresh)
        
        layout.addLayout(header_layout)
        
        # Tree Widget layout
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Timestamp / Item", "Details"])
        self.tree.setColumnWidth(0, 300)
        
        layout.addWidget(self.tree)

    def load_history(self):
        self.tree.clear()
        user_data = self.user_system.get_user_data()
        history = user_data.get("scan_history", [])
        
        # Load from newest to oldest
        for entry in reversed(history):
            item = QTreeWidgetItem([f"{entry['timestamp']} - {entry['type']}", ""])
            
            data = entry['data']
            if entry['type'] == "Port Scan" and 'open_ports' in data:
                QTreeWidgetItem(item, ["Target", str(data.get('target', 'Unknown'))])
                ports_item = QTreeWidgetItem(item, [f"Open Ports ({len(data['open_ports'])})", ""])
                for port_obj in data['open_ports']:
                    QTreeWidgetItem(ports_item, [f"Port {port_obj['port']}", port_obj['service']])
            
            elif entry['type'] == "Network Scan" and 'devices' in data:
                QTreeWidgetItem(item, ["Range", str(data.get('range', 'Unknown'))])
                devs_item = QTreeWidgetItem(item, [f"Devices Found ({len(data['devices'])})", ""])
                for dev in data['devices']:
                    QTreeWidgetItem(devs_item, [dev['ip'], f"{dev['mac']} ({dev['vendor']})"])
            
            self.tree.addTopLevelItem(item)
