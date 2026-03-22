import subprocess
import threading
from PySide6.QtWidgets import QLineEdit, QHBoxLayout, QPushButton, QTextEdit
from PySide6.QtCore import QObject, Signal, Qt
from .hash_generator import BaseToolPage

class PingWorker(QObject):
    output = Signal(str)
    finished = Signal()
    
    def run(self, host):
        try:
            # -n 4 runs 4 pings on Windows
            cmd = ["ping", "-n", "4", host]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            for line in iter(process.stdout.readline, ''):
                self.output.emit(line.strip())
                
            process.stdout.close()
            process.wait()
        except Exception as e:
            self.output.emit(f"Hata: {e}")
        finally:
            self.finished.emit()

class PingToolPage(BaseToolPage):
    def __init__(self):
        super().__init__("Ping Aracı", 
                         "Belirtilen bir IP adresine veya web sitesine ICMP (Ping) paketleri göndererek "
                         "sistemin ayakta / ulaşılabilir olup olmadığını kontrol eder.")
        
        input_layout = QHBoxLayout()
        self.input_host = QLineEdit()
        self.input_host.setPlaceholderText("IP veya Domain (örn: google.com veya 192.168.1.1)")
        input_layout.addWidget(self.input_host)
        
        self.btn_ping = QPushButton("Ping Gönder")
        self.btn_ping.clicked.connect(self.start_ping)
        input_layout.addWidget(self.btn_ping)
        
        self.layout.addLayout(input_layout)
        
        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setStyleSheet("font-family: monospace;")
        self.layout.addWidget(self.result_box)
        
        self.worker = PingWorker()
        self.worker.output.connect(self.append_output)
        self.worker.finished.connect(self.ping_done)

    def start_ping(self):
        host = self.input_host.text().strip()
        if not host: return
        
        self.btn_ping.setEnabled(False)
        self.result_box.clear()
        self.result_box.append(f"> ping {host}\n")
        
        t = threading.Thread(target=self.worker.run, args=(host,))
        t.daemon = True
        t.start()
        
    def append_output(self, text):
        self.result_box.append(text)
        
    def ping_done(self):
        self.result_box.append("\n[Ping işlemi tamamlandı]")
        self.btn_ping.setEnabled(True)
