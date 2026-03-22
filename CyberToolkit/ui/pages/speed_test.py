from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QProgressBar
from PySide6.QtCore import Qt
from modules.speed_test import SpeedTest

class SpeedTestPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        self.tester = SpeedTest()
        self.tester.progress.connect(self.on_progress)
        self.tester.result_found.connect(self.on_result)
        
        title = QLabel("Ağ Hız Testi (Ping Yükü & Bant Genişliği)")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #3b82f6;")
        self.layout.addWidget(title)
        
        desc = QLabel("Bilgisayarınızın gecikme (Latency), kayıp (Jitter) oranlarını ve gerçek internet indirme hızını (Bandwidth) harici sitelere reklam göstermeden yerel olarak ölçer.")
        desc.setWordWrap(True)
        self.layout.addWidget(desc)
        
        self.btn_start = QPushButton("🚀 Hız Testini Başlat")
        self.btn_start.setStyleSheet("padding: 12px; background-color: #3b82f6; color: white; font-weight: bold; font-size: 16px;")
        self.btn_start.clicked.connect(self.start_test)
        self.layout.addWidget(self.btn_start)
        
        self.lbl_status = QLabel("Durum: Bekliyor...")
        self.lbl_status.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.lbl_status)
        
        self.progress = QProgressBar()
        self.layout.addWidget(self.progress)
        
        # Results area
        self.lbl_results = QLabel("")
        self.lbl_results.setStyleSheet("font-size: 18px; line-height: 1.5;")
        self.lbl_results.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.lbl_results)

    def start_test(self):
        self.lbl_results.setText("")
        self.progress.setValue(0)
        self.lbl_status.setText("Test başlatıldı...")
        self.btn_start.setEnabled(False)
        self.tester.run_test()

    def on_progress(self, val, msg):
        self.progress.setValue(val)
        self.lbl_status.setText(msg)

    def on_result(self, max_ping, avg_ping, mbps):
        self.btn_start.setEnabled(True)
        self.lbl_status.setText("Tamamlandı.")
        
        res = (f"<b>Ortalama Gecikme (Ping):</b> {avg_ping} ms<br>"
               f"<b>Maksimum Jitter (Kayıp Tepesi):</b> {max_ping} ms<br>"
               f"<br><b style='font-size: 26px; color: #10b981;'>Tahmini İndirme Hızı:<br>{mbps} Mbps</b>")
        
        self.lbl_results.setText(res)
