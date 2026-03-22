import ipaddress
from PySide6.QtWidgets import QLineEdit, QHBoxLayout, QPushButton, QTextEdit
from .hash_generator import BaseToolPage

class SubnetCalculatorPage(BaseToolPage):
    def __init__(self):
        super().__init__("Alt Ağ Hesaplayıcı", 
                         "Bir IP adresi ve CIDR (/24, /16 vb.) değeri alarak, alt ağın (subnet) başlangıç, "
                         "bitiş, yayın (broadcast) adreslerini ve toplam kullanılabilir host sayısını hesaplar.")
        
        input_layout = QHBoxLayout()
        self.input_ip = QLineEdit()
        self.input_ip.setPlaceholderText("IP ve CIDR girin (Örn: 192.168.1.10/24)")
        input_layout.addWidget(self.input_ip)
        
        btn_calc = QPushButton("Hesapla")
        btn_calc.clicked.connect(self.calculate_subnet)
        input_layout.addWidget(btn_calc)
        
        self.layout.addLayout(input_layout)
        
        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setStyleSheet("font-family: monospace; font-size: 14px;")
        self.layout.addWidget(self.result_box)

    def calculate_subnet(self):
        ip_str = self.input_ip.text().strip()
        if not ip_str: return
        
        try:
            net = ipaddress.IPv4Network(ip_str, strict=False)
            
            res = (
                f"Ağ Adresi (Network):      {net.network_address}\n"
                f"Yayın Adresi (Broadcast): {net.broadcast_address}\n"
                f"Ağ Maskesi (Netmask):     {net.netmask}\n"
                f"Kullanılabilir Host:      {net.num_addresses - 2 if net.num_addresses > 2 else 0}\n"
                f"CIDR Notasyonu:           /{net.prefixlen}\n\n"
            )
            
            if net.num_addresses > 2:
                hosts = list(net.hosts())
                res += f"İlk IP:                   {hosts[0]}\n"
                res += f"Son IP:                   {hosts[-1]}\n"
                
            self.result_box.setPlainText(res)
        except Exception as e:
            self.result_box.setPlainText(f"Hata: Geçersiz IP/CIDR formatı.\n{e}")
