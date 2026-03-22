from urllib.parse import quote, unquote
from PySide6.QtWidgets import QTextEdit, QHBoxLayout, QPushButton
from .hash_generator import BaseToolPage

class UrlToolPage(BaseToolPage):
    def __init__(self):
        super().__init__("URL Kodlayıcı", 
                         "Web URL'lerindeki özel karakterleri (boşluk, & vs.) tarayıcıların anlayabileceği "
                         "% (Yüzde) kodlama formatına çevirir (Encode) veya karmaşık URL'leri çözer (Decode).")
        
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("URL metnini buraya girin...")
        self.layout.addWidget(self.input_text)
        
        btn_layout = QHBoxLayout()
        btn_enc = QPushButton("URL Encode Yarat")
        btn_enc.clicked.connect(self.encode_url)
        btn_layout.addWidget(btn_enc)
        
        btn_dec = QPushButton("URL Decode Çöz")
        btn_dec.clicked.connect(self.decode_url)
        btn_layout.addWidget(btn_dec)
        
        self.layout.addLayout(btn_layout)
        
        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setPlaceholderText("Sonuç burada görünecek...")
        self.layout.addWidget(self.result_box)

    def encode_url(self):
        text = self.input_text.toPlainText()
        if not text: return
        res = quote(text, safe='')
        self.result_box.setPlainText(res)

    def decode_url(self):
        text = self.input_text.toPlainText()
        if not text: return
        res = unquote(text)
        self.result_box.setPlainText(res)
