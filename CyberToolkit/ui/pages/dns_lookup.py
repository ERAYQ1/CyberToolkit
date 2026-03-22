import socket
import threading
from PySide6.QtWidgets import QLineEdit, QHBoxLayout, QPushButton, QTextEdit
from .hash_generator import BaseToolPage

class DnsLookupPage(BaseToolPage):
    def __init__(self):
        super().__init__("DNS Sorgulama Aracı", 
                         "Bir alan adının (domain) IP adresini (A Kaydı) veya bir IP adresinin işaret ettiği "
                         "ters DNS adını bulur.")
        
        input_layout = QHBoxLayout()
        self.input_host = QLineEdit()
        self.input_host.setPlaceholderText("Domain veya IP adresi girin...")
        input_layout.addWidget(self.input_host)
        
        btn_lookup = QPushButton("Sorgula")
        btn_lookup.clicked.connect(self.start_lookup)
        input_layout.addWidget(btn_lookup)
        
        self.layout.addLayout(input_layout)
        
        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.layout.addWidget(self.result_box)

    def start_lookup(self):
        target = self.input_host.text().strip()
        if not target: return
        
        self.result_box.setPlainText(f"Sorgulanıyor: {target} ...\n")
        
        def _lookup():
            try:
                # Is it an IP?
                socket.inet_aton(target)
                is_ip = True
            except socket.error:
                is_ip = False
                
            try:
                if is_ip:
                    res = socket.gethostbyaddr(target)
                    out = f"IP Adresi: {target}\nDNS Gerçek Adı (PTR): {res[0]}\nEkstra İsimler: {', '.join(res[1])}"
                else:
                    ip = socket.gethostbyname(target)
                    out = f"Domain: {target}\nIP Adresi (A Kaydı): {ip}"
                    
                # Safe GUI update approach ideally uses Signals, but readOnly text update in quick thread is usually OK in python if minimal
                self.result_box.append("\n" + out)
            except Exception as e:
                self.result_box.append(f"\nSorgu başarısız: {e}")

        threading.Thread(target=_lookup, daemon=True).start()
