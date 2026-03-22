from PySide6.QtWidgets import QPushButton, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt
from ui.pages.hash_generator import BaseToolPage
from modules.cam_mic_monitor import DeviceMonitor

class CamMicMonitorPage(BaseToolPage):
    def __init__(self):
        super().__init__("Kamera & Mikrofon Bekçisi", 
                         "Arka planda sessizce bekler. İzniniz dışında herhangi bir uygulama veya kişi kameranızı ya da mikrofonunuzu aktifleştirirse sizi hemen kırmızı bir uyarıyla bilgilendirir.")
        
        self.btn_toggle = QPushButton("Acil Durum İzlemesini Başlat (Arka Plan)")
        self.btn_toggle.clicked.connect(self.toggle_monitor)
        self.layout.addWidget(self.btn_toggle)
        
        self.list_alerts = QListWidget()
        self.layout.addWidget(self.list_alerts)
        
        self.monitor = DeviceMonitor()
        self.monitor.alert_triggered.connect(self.on_alert)
        self.is_monitoring = False

    def toggle_monitor(self):
        if not self.is_monitoring:
            self.monitor.start_monitor()
            self.btn_toggle.setText("İzlemeyi Durdur")
            self.btn_toggle.setStyleSheet("background-color: #ef4444; color: white;")
            self.is_monitoring = True
            
            # Start message
            self.list_alerts.addItem(QListWidgetItem("🟢 İzleme aktif. Bekleniyor..."))
        else:
            self.monitor.stop_monitor()
            self.btn_toggle.setText("Acil Durum İzlemesini Başlat (Arka Plan)")
            self.btn_toggle.setStyleSheet("")
            self.is_monitoring = False
            self.list_alerts.addItem(QListWidgetItem("🔴 İzleme durduruldu."))

    def on_alert(self, device, app, time_str):
        msg = f"[{time_str}] UYARI! '{app}' isimli uygulama şu an {device} aygıtınıza erişim sağlıyor!"
        item = QListWidgetItem(msg)
        item.setForeground(Qt.red)
        self.list_alerts.addItem(item)
