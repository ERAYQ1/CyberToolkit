import random
import string
from PySide6.QtWidgets import QLineEdit, QPushButton, QSlider, QLabel
from PySide6.QtCore import Qt
from .hash_generator import BaseToolPage

class PasswordGeneratorPage(BaseToolPage):
    def __init__(self):
        super().__init__("Güvenli Şifre Oluşturucu", 
                         "Kırılması zor, harf, rakam ve özel karakterlerden oluşan rastgele güvenli şifreler üretir.")
        
        self.lbl_len = QLabel("Uzunluk: 16")
        self.layout.addWidget(self.lbl_len)
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(8)
        self.slider.setMaximum(128)
        self.slider.setValue(16)
        self.slider.valueChanged.connect(self.update_length_label)
        self.layout.addWidget(self.slider)
        
        btn_gen = QPushButton("Şifre Üret")
        btn_gen.clicked.connect(self.generate_password)
        self.layout.addWidget(btn_gen)
        
        self.result_box = QLineEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setAlignment(Qt.AlignCenter)
        self.result_box.setStyleSheet("font-family: monospace; font-size: 20px; padding: 10px;")
        self.layout.addWidget(self.result_box)
        
        self.layout.addStretch()

    def update_length_label(self, val):
        self.lbl_len.setText(f"Uzunluk: {val}")

    def generate_password(self):
        length = self.slider.value()
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        
        # Ensure at least one of each
        pwd = [
            random.choice(string.ascii_lowercase),
            random.choice(string.ascii_uppercase),
            random.choice(string.digits),
            random.choice("!@#$%^&*")
        ]
        
        for _ in range(length - 4):
            pwd.append(random.choice(chars))
            
        random.shuffle(pwd)
        self.result_box.setText("".join(pwd))
