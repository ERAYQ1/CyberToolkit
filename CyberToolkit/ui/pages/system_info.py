import psutil
import platform
from PySide6.QtWidgets import QTextEdit, QPushButton
from .hash_generator import BaseToolPage

class SystemInfoPage(BaseToolPage):
    def __init__(self):
        super().__init__("Sistem Bilgisi", 
                         "Geçerli cihazınızın (Bilgisayarınızın) donanım kaynaklarını, işletim sistemi "
                         "versiyonunu ve aktif kaynak tüketimlerini gösterir.")
        
        self.btn_refresh = QPushButton("Bilgileri Yenile")
        self.btn_refresh.clicked.connect(self.load_info)
        self.layout.addWidget(self.btn_refresh)
        
        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setStyleSheet("font-family: monospace; font-size: 14px;")
        self.layout.addWidget(self.result_box)
        
        self.load_info()

    def load_info(self):
        try:
            uname = platform.uname()
            svmem = psutil.virtual_memory()
            cpufreq = psutil.cpu_freq()
            cores = psutil.cpu_count(logical=True)
            
            def get_size(bytes, suffix="B"):
                factor = 1024
                for unit in ["", "K", "M", "G", "T", "P"]:
                    if bytes < factor:
                        return f"{bytes:.2f}{unit}{suffix}"
                    bytes /= factor
            
            info = f"=== İŞLETİM SİSTEMİ ===\n"
            info += f"Sistem: {uname.system}\n"
            info += f"Cihaz Adı: {uname.node}\n"
            info += f"Sürüm: {uname.release}\n"
            info += f"Mimari: {uname.machine}\n\n"
            
            info += f"=== İŞLEMCİ (CPU) ===\n"
            info += f"Çekirdek: {cores}\n"
            if cpufreq:
                info += f"Maks Frekans: {cpufreq.max:.2f}Mhz\n"
            info += f"Kullanım: {psutil.cpu_percent()}%\n\n"
            
            info += f"=== RAM (BELLEK) ===\n"
            info += f"Toplam: {get_size(svmem.total)}\n"
            info += f"Kullanılan: {get_size(svmem.used)} ({svmem.percent}%)\n"
            info += f"Boş: {get_size(svmem.available)}\n"
            
            self.result_box.setPlainText(info)
        except Exception as e:
            self.result_box.setPlainText(f"Bilgi yüklenemedi: {e}")
