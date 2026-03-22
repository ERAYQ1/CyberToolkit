from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QTextEdit
from ui.pages.hash_generator import BaseToolPage
from modules.usb_vaccine import USBVaccine

class USBVaccinePage(BaseToolPage):
    def __init__(self):
        super().__init__("USB Aşısı", 
                         "Bilgisayarınıza takılan yabancı flash belleklerden (USB) otomatik olarak fidye yazılımı ve virüs bulaşmasını tamamen engellemek için, 'Auto-Run' (Otomatik Kullan) zafiyetlerini Windows Kayıt Defterinden kalıcı olarak kapatır.")
        
        self.vaccine = USBVaccine()
        
        self.lbl_status = QLabel("Durum: Bilinmiyor")
        self.lbl_status.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout.addWidget(self.lbl_status)
        
        btn_layout = QHBoxLayout()
        self.btn_apply = QPushButton("💉 Bilgisayarı Aşıla")
        self.btn_apply.setStyleSheet("background-color: #10b981; color: white;")
        self.btn_apply.clicked.connect(self.apply_vaccine)
        btn_layout.addWidget(self.btn_apply)
        
        self.btn_remove = QPushButton("Düzelt (Aşıyı Çıkar)")
        self.btn_remove.setStyleSheet("background-color: #ef4444; color: white;")
        self.btn_remove.clicked.connect(self.remove_vaccine)
        btn_layout.addWidget(self.btn_remove)
        
        self.layout.addLayout(btn_layout)
        
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.layout.addWidget(self.log_box)
        
        self.check_status()

    def check_status(self):
        status = self.vaccine.check_status()
        if status == -1:
            self.lbl_status.setText("Durum: Erişim Reddedildi (Yönetici İzni Gerekli)")
            self.lbl_status.setStyleSheet("color: #ef4444;")
        elif status:
            self.lbl_status.setText("Durum: GÜVENDE (Otomatik Çalıştırma Tamamen Kapalı)")
            self.lbl_status.setStyleSheet("color: #10b981;")
        else:
            self.lbl_status.setText("Durum: RİSKLİ (Flash bellekler takıldığında otomatik kod çalıştırabilir)")
            self.lbl_status.setStyleSheet("color: #f59e0b;")

    def apply_vaccine(self):
        success, msg = self.vaccine.apply_vaccine()
        self.log_box.append(f"> İşlem: {msg}")
        self.check_status()

    def remove_vaccine(self):
        success, msg = self.vaccine.remove_vaccine()
        self.log_box.append(f"> İşlem: {msg}")
        self.check_status()
