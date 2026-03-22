import random
from PySide6.QtWidgets import QLineEdit, QHBoxLayout, QPushButton, QLabel, QFormLayout
from .hash_generator import BaseToolPage

class MacToolPage(BaseToolPage):
    def __init__(self):
        super().__init__("MAC Denetleyici & Üretici", 
                         "Ağ cihazlarının fiziksel adresi olan MAC (Media Access Control) adreslerini rastgele oluşturur "
                         "veya formatının doğruluğunu denetler.")
        
        form_layout = QFormLayout()
        
        self.lbl_generated = QLineEdit()
        self.lbl_generated.setReadOnly(True)
        self.lbl_generated.setStyleSheet("font-family: monospace; font-size: 16px;")
        
        btn_gen = QPushButton("Rastgele MAC Oluştur")
        btn_gen.clicked.connect(self.generate_mac)
        
        form_layout.addRow(btn_gen, self.lbl_generated)
        
        self.layout.addLayout(form_layout)
        
        self.layout.addSpacing(20)
        
        self.input_mac = QLineEdit()
        self.input_mac.setPlaceholderText("Denetlenecek MAC (Örn: 00:1A:2B:3C:4D:5E)")
        self.layout.addWidget(self.input_mac)
        
        btn_validate = QPushButton("MAC Doğrula")
        btn_validate.clicked.connect(self.validate_mac)
        self.layout.addWidget(btn_validate)
        
        self.lbl_val_res = QLabel("Sonuç: Bekleniyor")
        self.lbl_val_res.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")
        self.layout.addWidget(self.lbl_val_res)
        
        self.layout.addStretch()

    def generate_mac(self):
        mac = [ 0x00, 0x16, 0x3e,
                random.randint(0x00, 0x7f),
                random.randint(0x00, 0xff),
                random.randint(0x00, 0xff) ]
        res = ':'.join(map(lambda x: "%02x" % x, mac)).upper()
        self.lbl_generated.setText(res)

    def validate_mac(self, text=""):
        mac = self.input_mac.text().strip()
        import re
        if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()):
            self.lbl_val_res.setText("Sonuç: GEÇERLİ MAC ADRESİ ✅")
            self.lbl_val_res.setStyleSheet("color: #10b981; font-size: 16px; font-weight: bold;")
        else:
            self.lbl_val_res.setText("Sonuç: GEÇERSİZ MAC ADRESİ ❌")
            self.lbl_val_res.setStyleSheet("color: #ef4444; font-size: 16px; font-weight: bold;")
