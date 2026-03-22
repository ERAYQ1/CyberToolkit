from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt
from modules.connection_monitor import ConnectionMonitor
from .dashboard import create_info_box

class ConnectionMonitorPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Canlı Bağlantılar")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        layout.addWidget(create_info_box("Bu özellik nedir?", "Bilgisayarınızın arkaplanında internet ile konuşan tüm uygulamaları (Chrome, Discord, Virüs vs.) ve bağlandıkları IP'leri saniye saniye canlı listeler."))
        
        ctrl_layout = QHBoxLayout()
        self.btn_toggle = QPushButton("İzlemeyi Başlat")
        self.btn_toggle.clicked.connect(self.toggle_monitor)
        ctrl_layout.addWidget(self.btn_toggle)
        
        layout.addLayout(ctrl_layout)
        
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["İşlem (Uygulama)", "Yerel IP", "Uzak IP", "Durum", "PID"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("background-color: #1e293b; color: #e2e8f0; gridline-color: #334155; border: 1px solid #334155;")
        self.table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #334155; color: white; border: 1px solid #475569; }")
        layout.addWidget(self.table)
        
        self.monitor = ConnectionMonitor()
        self.monitor.connections_updated.connect(self.update_table)
        self.is_monitoring = False

    def toggle_monitor(self):
        if not self.is_monitoring:
            self.monitor.start_monitor()
            self.btn_toggle.setText("İzlemeyi Durdur")
            self.btn_toggle.setStyleSheet("background-color: #ef4444; color: white;")
            self.is_monitoring = True
        else:
            self.monitor.stop_monitor()
            self.btn_toggle.setText("İzlemeyi Başlat")
            self.btn_toggle.setStyleSheet("")
            self.is_monitoring = False

    def update_table(self, connections):
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        
        for conn in connections:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            p_item = QTableWidgetItem(conn["process"] or "Bilinmiyor")
            l_item = QTableWidgetItem(conn["local"])
            r_item = QTableWidgetItem(conn["remote"])
            s_item = QTableWidgetItem(conn["status"])
            pid_item = QTableWidgetItem(str(conn["pid"]))
            
            if conn["suspicious"]:
                for item in [p_item, l_item, r_item, s_item, pid_item]:
                    item.setForeground(Qt.red)
                    
            self.table.setItem(row, 0, p_item)
            self.table.setItem(row, 1, l_item)
            self.table.setItem(row, 2, r_item)
            self.table.setItem(row, 3, s_item)
            self.table.setItem(row, 4, pid_item)
            
        self.table.setSortingEnabled(True)

    def hideEvent(self, event):
        if self.is_monitoring:
            self.toggle_monitor()
        super().hideEvent(event)
