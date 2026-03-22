from PySide6.QtWidgets import QPushButton, QTextEdit
from ui.pages.hash_generator import BaseToolPage
from modules.honeypot import Honeypot

class HoneypotPage(BaseToolPage):
    def __init__(self):
        super().__init__("Siber Kapan (Honeypot)", 
                         "Kendi bilgisayarınızda bilerek açık FTP (21) veya HTTP (8080) soketleri çalıştırıp 'tuzak' kurar. Sizin bulunduğunuz aynı Wi-Fi ağında (Örn: Kafe, Yurt) birisi bilgisayarınıza hack denemesi veya port taraması yaparsa hemen alarm çalar.")
        
        self.btn_toggle = QPushButton("Ağ İçi Siber Kapanı Kur (Tuzak Başlat)")
        self.btn_toggle.clicked.connect(self.toggle_trap)
        self.layout.addWidget(self.btn_toggle)
        
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setStyleSheet("color: #10b981; font-family: monospace;")
        self.layout.addWidget(self.log_box)
        
        self.honeypot = Honeypot()
        self.honeypot.alert_triggered.connect(self.on_alert)
        self.is_trapping = False

    def toggle_trap(self):
        if not self.is_trapping:
            self.honeypot.start_trap()
            self.btn_toggle.setText("Tuzakları Devre Dışı Bırak")
            self.btn_toggle.setStyleSheet("background-color: #ef4444; color: white;")
            self.is_trapping = True
            self.log_box.append("> Siber Kapan Gevşetildi. Ortam Dinleniyor... (Port 21, 2222, 8080 açık)")
        else:
            self.honeypot.stop_trap()
            self.btn_toggle.setText("Ağ İçi Siber Kapanı Kur (Tuzak Başlat)")
            self.btn_toggle.setStyleSheet("")
            self.is_trapping = False
            self.log_box.append("> Siber Kapan Kapatıldı.")

    def on_alert(self, ip, time_str, port):
        msg = f"🚨 UYARI! [{time_str}] BİRİSİ CİHAZINA SIZMAYA ÇALIŞTI!\n" \
              f"-> Hedef Port: {port} (Tuzak Portu)\n" \
              f"-> Saldırgan IP'si: {ip}\n"
        self.log_box.append(msg)
