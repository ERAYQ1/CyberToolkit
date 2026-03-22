from PySide6.QtWidgets import QLabel, QPushButton, QTextEdit
from ui.pages.hash_generator import BaseToolPage
from modules.win_hardening import WindowsHardening

class WindowsHardeningPage(BaseToolPage):
    def __init__(self):
        super().__init__("Windows Güvenlik Sıkılaştırma", 
                         "İşletim sisteminizin kalesi olan Windows Defender Anti-Virüsünün ve Kullanıcı Hesabı Denetiminin (UAC) açık ve zırhlı durumda olup olmadığını tek yerden denetlemenizi sağlar.")
        
        self.hardening = WindowsHardening()
        
        self.layout.addWidget(QLabel("Mevcut Güvenlik Duvarı Ve Zırh Durumu:"))
        
        self.txt_status = QTextEdit()
        self.txt_status.setReadOnly(True)
        self.txt_status.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(self.txt_status)
        
        self.btn_uac = QPushButton("Windows UAC'yi (Kullanıcı Denetimini) Zorla Aç")
        self.btn_uac.clicked.connect(self.enable_uac)
        self.layout.addWidget(self.btn_uac)
        
        self.btn_refresh = QPushButton("Yenile")
        self.btn_refresh.clicked.connect(self.refresh_status)
        self.layout.addWidget(self.btn_refresh)
        
        self.refresh_status()

    def refresh_status(self):
        rep = self.hardening.get_security_report()
        res = ""
        
        if rep["UAC_Active"]:
            res += "✅ UAC (Kullanıcı Hesabı Denetimi) AKTİF.\n"
        else:
            res += "❌ UAC KAPALI! Tehlike: Uygulamalar sizden izin almadan yönetici yetkisine erişebilir.\n"
            
        res += "\n"
        
        if rep["Defender_Active"] == True:
            res += "✅ Windows Defender Anti-Virüs AKTİF.\n"
        elif rep["Defender_Active"] == False:
            res += "❌ Windows Defender KAPALI! Cihazınız virüslere karşı savunmasız duruyor.\n"
        else:
            res += "⚠️ Windows Defender durumu tam okunamadı (Yönetici yetkisi gerektirebilir).\n"
            
        self.txt_status.setPlainText(res)

    def enable_uac(self):
        success, msg = self.hardening.enable_uac()
        self.txt_status.append(f"\n> İşlem Geri Dönüşü: {msg}")
        self.refresh_status()
