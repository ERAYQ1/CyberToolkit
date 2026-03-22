import base64
from PySide6.QtWidgets import QTextEdit, QHBoxLayout, QPushButton
from .hash_generator import BaseToolPage

class Base64ToolPage(BaseToolPage):
    def __init__(self):
        super().__init__("Base64 Dönüştürücü", 
                         "Metinleri Base64 formatına çevirir veya Base64 formatındaki metinleri normal okunabilir hale getirir. "
                         "Temel veri gizleme metodudur ancak şifreleme DEĞİLDİR.")
        
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Çevrilecek metni buraya girin...")
        self.layout.addWidget(self.input_text)
        
        btn_layout = QHBoxLayout()
        btn_enc = QPushButton("Base64 ile Şifrele (Encode)")
        btn_enc.clicked.connect(self.encode_b64)
        btn_layout.addWidget(btn_enc)
        
        btn_dec = QPushButton("Base64'ü Çöz (Decode)")
        btn_dec.clicked.connect(self.decode_b64)
        btn_layout.addWidget(btn_dec)
        
        self.layout.addLayout(btn_layout)
        
        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setPlaceholderText("Sonuç burada görünecek...")
        self.layout.addWidget(self.result_box)

    def encode_b64(self):
        text = self.input_text.toPlainText().encode('utf-8')
        if not text: return
        try:
            res = base64.b64encode(text).decode('utf-8')
            self.result_box.setPlainText(res)
        except Exception as e:
            self.result_box.setPlainText(f"Hata: {e}")

    def decode_b64(self):
        text = self.input_text.toPlainText().strip()
        if not text: return
        try:
            res = base64.b64decode(text).decode('utf-8')
            self.result_box.setPlainText(res)
        except Exception:
            self.result_box.setPlainText("Hata: Geçersiz Base64 verisi.")
