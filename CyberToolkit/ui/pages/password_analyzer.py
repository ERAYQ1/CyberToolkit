from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PySide6.QtCore import Qt
from modules.password_analyzer import PasswordAnalyzer
from .dashboard import create_info_box

class PasswordAnalyzerPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Şifre Analizcisi")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        layout.addWidget(create_info_box("Bu özellik nedir?", "Bir parolanın karmaşıklığını ve tahmin edilebilirliğini ölçer. Olası kırılma/çözülme süresini hesaplayarak matematiksel bir tahmin yürütür."))
        
        self.input_pwd = QLineEdit()
        self.input_pwd.setEchoMode(QLineEdit.Password)
        self.input_pwd.setPlaceholderText("Analiz edilecek şifreyi girin...")
        self.input_pwd.textChanged.connect(self.analyze_pwd)
        layout.addWidget(self.input_pwd)
        
        self.btn_toggle = QPushButton("Şifreyi Göster")
        self.btn_toggle.clicked.connect(self.toggle_visibility)
        layout.addWidget(self.btn_toggle)
        
        self.lbl_strength = QLabel("Güç: N/A")
        self.lbl_strength.setStyleSheet("font-size: 18px;")
        layout.addWidget(self.lbl_strength)
        
        self.lbl_time = QLabel("Tahmini Kırılma Süresi: N/A")
        self.lbl_time.setStyleSheet("font-size: 16px; color: #94a3b8;")
        layout.addWidget(self.lbl_time)
        
        self.txt_suggestions = QTextEdit()
        self.txt_suggestions.setReadOnly(True)
        self.txt_suggestions.setPlaceholderText("Öneriler burada görünecek...")
        layout.addWidget(self.txt_suggestions)
        
        self.analyzer = PasswordAnalyzer()

    def toggle_visibility(self):
        if self.input_pwd.echoMode() == QLineEdit.Password:
            self.input_pwd.setEchoMode(QLineEdit.Normal)
            self.btn_toggle.setText("Şifreyi Gizle")
        else:
            self.input_pwd.setEchoMode(QLineEdit.Password)
            self.btn_toggle.setText("Şifreyi Göster")

    def analyze_pwd(self, text):
        if not text:
            self.lbl_strength.setText("Güç: N/A")
            self.lbl_strength.setStyleSheet("font-size: 18px;")
            self.lbl_time.setText("Tahmini Kırılma Süresi: N/A")
            self.txt_suggestions.clear()
            return

        result = self.analyzer.analyze(text)
        
        # Translation of simple rules map
        tr_strength = {"Weak": "Zayıf", "Medium": "Orta", "Strong": "Güçlü"}.get(result['strength'], result['strength'])
        
        self.lbl_strength.setText(f"Güç: {tr_strength} ({result['score']}/{result['max_score']})")
        self.lbl_strength.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {result['color']};")
        
        # Keep time as is, usually self._format_time handles it or it's English, we can just say "Time"
        self.lbl_time.setText(f"Tahmini Kırılma Süresi: {result['crack_time']}")
        
        if result['suggestions']:
            self.txt_suggestions.setPlainText("Geliştirmek için öneriler:\n" + "\n".join(f"- {s}" for s in result['suggestions']))
        else:
            self.txt_suggestions.setPlainText("Şifre oldukça güçlü görünüyor. Ek öneri yok.")
