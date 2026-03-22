from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                               QFrame, QListWidget)
from PySide6.QtGui import QFont

from modules.password_analyzer import PasswordAnalyzer

class PasswordAnalyzerPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        header = QLabel("Password Analyzer")
        header.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.setStyleSheet("color: #00e676;")
        layout.addWidget(header)
        
        layout.addWidget(QLabel("Type a password below to evaluate its strength (calculated locally, NOT sent anywhere)."))
        
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Enter password...")
        self.pass_input.setEchoMode(QLineEdit.Normal) # Show characters so user sees what they type
        self.pass_input.textChanged.connect(self.analyze_password)
        layout.addWidget(self.pass_input)
        
        # Results frame
        self.result_frame = QFrame()
        res_layout = QVBoxLayout(self.result_frame)
        
        self.lbl_strength = QLabel("Strength: None")
        self.lbl_strength.setFont(QFont("Segoe UI", 16, QFont.Bold))
        
        self.lbl_crack_time = QLabel("Estimated crack time: 0 seconds")
        self.lbl_crack_time.setFont(QFont("Segoe UI", 12))
        
        self.lbl_entropy = QLabel("Entropy: 0 bits")
        self.lbl_entropy.setFont(QFont("Segoe UI", 10))
        
        res_layout.addWidget(self.lbl_strength)
        res_layout.addWidget(self.lbl_crack_time)
        res_layout.addWidget(self.lbl_entropy)
        
        layout.addWidget(self.result_frame)
        
        # Suggestions
        layout.addWidget(QLabel("Suggestions for Improvement:"))
        self.suggestions_list = QListWidget()
        self.suggestions_list.setStyleSheet("background-color: transparent; border: none; color: #ffb86c;")
        layout.addWidget(self.suggestions_list)
        
        layout.addStretch()

    def analyze_password(self, text):
        res = PasswordAnalyzer.analyze(text)
        
        # Update labels
        self.lbl_strength.setText(f"Strength: {res['strength']} (Score: {res['score']})")
        self.lbl_crack_time.setText(f"Estimated crack time: {res['crack_time']}")
        self.lbl_entropy.setText(f"Mathematical Entropy: {res['entropy']} bits")
        
        # Color code strength
        color = "#ff5555" # red
        if res['strength'] == "Medium":
            color = "#ffb86c" # orange
        elif "Strong" in res['strength']:
            color = "#00e676" # green
            
        self.lbl_strength.setStyleSheet(f"color: {color};")
        
        # Update suggestions
        self.suggestions_list.clear()
        for s in res['suggestions']:
            self.suggestions_list.addItem(f"• {s}")
