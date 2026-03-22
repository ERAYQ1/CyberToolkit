import base64
from PySide6.QtWidgets import QTextEdit, QHBoxLayout, QPushButton, QLineEdit
from .hash_generator import BaseToolPage

class TextEncryptorPage(BaseToolPage):
    def __init__(self):
        super().__init__("Metin Şifreleyici (XOR)", 
                         "Basit bir XOR (Özel Veya) mantığı ile metinlerinizi bir anahtar kelime aracılığıyla "
                         "şifreler veya şifreyi çözer. Gizli mesajlaşma için kullanılabilir.")
        
        self.input_key = QLineEdit()
        self.input_key.setPlaceholderText("Şifreleme Anahtarı (Key) girin...")
        self.layout.addWidget(self.input_key)
        
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Şifrelenecek VEYA Çözülecek metni girin...")
        self.layout.addWidget(self.input_text)
        
        btn_layout = QHBoxLayout()
        btn_enc = QPushButton("Şifrele")
        btn_enc.clicked.connect(self.encrypt_text)
        btn_layout.addWidget(btn_enc)
        
        btn_dec = QPushButton("Şifre Çöz")
        btn_dec.clicked.connect(self.decrypt_text)
        btn_layout.addWidget(btn_dec)
        
        self.layout.addLayout(btn_layout)
        
        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setPlaceholderText("Sonuç burada görünecek...")
        self.layout.addWidget(self.result_box)

    def _xor_crypt(self, text, key):
        if not key: key = "cyber"
        res = []
        for i in range(len(text)):
            c = text[i]
            k = key[i % len(key)]
            res.append(chr(ord(c) ^ ord(k)))
        return "".join(res)

    def encrypt_text(self):
        text = self.input_text.toPlainText()
        key = self.input_key.text()
        if not text: return
        
        encrypted = self._xor_crypt(text, key)
        # Encode res to base64 so it can be copy-pasted easily
        b64 = base64.b64encode(encrypted.encode('utf-8')).decode('utf-8')
        self.result_box.setPlainText(b64)

    def decrypt_text(self):
        b64_text = self.input_text.toPlainText().strip()
        key = self.input_key.text()
        if not b64_text: return
        
        try:
            raw = base64.b64decode(b64_text).decode('utf-8')
            decrypted = self._xor_crypt(raw, key)
            self.result_box.setPlainText(decrypted)
        except Exception:
            self.result_box.setPlainText("Hata: Çözülecek metin Base64 formatında olmalıdır.")
