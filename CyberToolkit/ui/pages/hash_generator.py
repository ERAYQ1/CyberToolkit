import hashlib
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit

class BaseToolPage(QWidget):
    """A helper base tracking the info box logic."""
    def __init__(self, title, info_text):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        self.layout.addWidget(lbl_title)
        
        # Info Box
        self.info_box = QWidget()
        self.info_box.setStyleSheet("background-color: #1e293b; border-left: 4px solid #3b82f6; padding: 10px; margin-bottom: 20px;")
        ib_layout = QVBoxLayout(self.info_box)
        ib_layout.setContentsMargins(10, 10, 10, 10)
        
        lbl_info_title = QLabel("ℹ️ Bu özellik nedir?")
        lbl_info_title.setStyleSheet("font-weight: bold; color: #3b82f6; border: none;")
        ib_layout.addWidget(lbl_info_title)
        
        lbl_info_text = QLabel(info_text)
        lbl_info_text.setWordWrap(True)
        lbl_info_text.setStyleSheet("color: #cbd5e1; border: none; font-size: 13px;")
        ib_layout.addWidget(lbl_info_text)
        
        self.layout.addWidget(self.info_box)

class HashGeneratorPage(BaseToolPage):
    def __init__(self):
        super().__init__("Hash Oluşturucu", 
                         "Yazdığınız metinlerin MD5, SHA-1, SHA-256 gibi kriptografik özetlerini çıkarır. "
                         "Parolaların veya dosyaların değişip değişmediğini kontrol etmek için sıklıkla kullanılır.")
        
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Hash'i alınacak metni buraya girin...")
        self.input_text.setMaximumHeight(100)
        self.input_text.textChanged.connect(self.calculate_hashes)
        self.layout.addWidget(self.input_text)
        
        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setPlaceholderText("Sonuçlar burada görünecek...")
        self.layout.addWidget(self.result_box)

    def calculate_hashes(self):
        text = self.input_text.toPlainText().encode('utf-8')
        if not text:
            self.result_box.clear()
            return
            
        md5 = hashlib.md5(text).hexdigest()
        sha1 = hashlib.sha1(text).hexdigest()
        sha256 = hashlib.sha256(text).hexdigest()
        sha512 = hashlib.sha512(text).hexdigest()
        
        out = f"--- MD5 ---\n{md5}\n\n"
        out += f"--- SHA-1 ---\n{sha1}\n\n"
        out += f"--- SHA-256 ---\n{sha256}\n\n"
        out += f"--- SHA-512 ---\n{sha512}"
        
        self.result_box.setPlainText(out)
