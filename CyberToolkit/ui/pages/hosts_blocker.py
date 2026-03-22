from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QTextEdit
from ui.components.base_tool_page import BaseToolPage
from modules.hosts_blocker import HostsBlocker

class HostsBlockerPage(BaseToolPage):
    def __init__(self):
        super().__init__("Hosts Kalkanı (Sistem Koruması)", 
                         "Windows 'hosts' dosyasını düzenleyerek sistem geneli bilinen zararlı (malware), reklam (adware) ve izleyici (telemetry) bağlantılarını kökten engeller. Tarayıcı eklentilerinden daha güçlüdür.")
        
        self.blocker = HostsBlocker()
        
        self.lbl_status = QLabel("Durum: Bilinmiyor")
        self.lbl_status.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout.addWidget(self.lbl_status)
        
        btn_layout = QHBoxLayout()
        self.btn_apply = QPushButton("🛡️ Kalkanı Aktif Et")
        self.btn_apply.setStyleSheet("background-color: #10b981; color: white;")
        self.btn_apply.clicked.connect(self.apply_shield)
        btn_layout.addWidget(self.btn_apply)
        
        self.btn_remove = QPushButton("❌ Kalkanı Kapat")
        self.btn_remove.setStyleSheet("background-color: #ef4444; color: white;")
        self.btn_remove.clicked.connect(self.remove_shield)
        btn_layout.addWidget(self.btn_remove)
        
        self.layout.addLayout(btn_layout)
        
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.layout.addWidget(self.log_box)
        
        self.check_status()

    def check_status(self):
        count = self.blocker.check_status()
        if count == -1:
            self.lbl_status.setText("Durum: Erişim Reddedildi (Yönetici İzni Gerekli)")
            self.lbl_status.setStyleSheet("color: #ef4444; font-size: 18px; font-weight: bold;")
        elif count > 0:
            self.lbl_status.setText("Durum: KORUNUYORSUNUZ (Aktif)")
            self.lbl_status.setStyleSheet("color: #10b981; font-size: 18px; font-weight: bold;")
        else:
            self.lbl_status.setText("Durum: KORUMASIZ (Kalkan Devre Dışı)")
            self.lbl_status.setStyleSheet("color: #f59e0b; font-size: 18px; font-weight: bold;")

    def apply_shield(self):
        success, msg = self.blocker.apply_protection()
        self.log_box.append(f"> Kalkanı Açma İsteği: {msg}")
        self.check_status()

    def remove_shield(self):
        success, msg = self.blocker.remove_protection()
        self.log_box.append(f"> Kalkanı Kapatma İsteği: {msg}")
        self.check_status()
