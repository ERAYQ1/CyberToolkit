import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QStackedWidget, QMessageBox, QFrame)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

class LoginWindow(QWidget):
    """
    The initial window the user sees to authenticate.
    Handles Login and Registration workflows via the UserSystem.
    """
    
    login_successful = Signal(str) # Emits username on success

    def __init__(self, user_system):
        super().__init__()
        self.user_system = user_system
        self.setWindowTitle("CyberToolkit - Access Portal")
        self.setFixedSize(400, 500)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # Main Card Frame
        self.card = QFrame()
        self.card.setObjectName("card")
        self.card.setFixedSize(320, 420)
        card_layout = QVBoxLayout(self.card)
        card_layout.setSpacing(20)

        # Logo / Title
        title_label = QLabel("CyberToolkit")
        title_font = QFont("Segoe UI", 24, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #00e676;") # Neon green
        
        subtitle_label = QLabel("Ethical Scanning Engine")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #888888; margin-bottom: 20px;")

        card_layout.addWidget(title_label)
        card_layout.addWidget(subtitle_label)

        # Stack for Login / Register Panels
        self.stack = QStackedWidget()
        
        self.login_widget = self.create_login_panel()
        self.register_widget = self.create_register_panel()
        
        self.stack.addWidget(self.login_widget)
        self.stack.addWidget(self.register_widget)
        
        card_layout.addWidget(self.stack)

        main_layout.addWidget(self.card)
        self.setLayout(main_layout)

    def create_login_panel(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignTop)
        
        self.login_user_input = QLineEdit()
        self.login_user_input.setPlaceholderText("Username")
        
        self.login_pass_input = QLineEdit()
        self.login_pass_input.setPlaceholderText("Password")
        self.login_pass_input.setEchoMode(QLineEdit.Password)
        
        btn_login = QPushButton("ACCESS SYSTEM")
        btn_login.clicked.connect(self.handle_login)
        
        btn_switch = QPushButton("Create Access Token")
        btn_switch.setStyleSheet("background-color: transparent; border: none; color: #888888;")
        btn_switch.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        layout.addWidget(self.login_user_input)
        layout.addWidget(self.login_pass_input)
        layout.addSpacing(20)
        layout.addWidget(btn_login)
        layout.addWidget(btn_switch)
        
        return widget

    def create_register_panel(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignTop)
        
        self.reg_user_input = QLineEdit()
        self.reg_user_input.setPlaceholderText("Desired Username")
        
        self.reg_pass_input = QLineEdit()
        self.reg_pass_input.setPlaceholderText("Secure Password")
        self.reg_pass_input.setEchoMode(QLineEdit.Password)
        
        btn_register = QPushButton("INITIALIZE PROFILE")
        btn_register.clicked.connect(self.handle_register)
        
        btn_switch = QPushButton("Return to Login")
        btn_switch.setStyleSheet("background-color: transparent; border: none; color: #888888;")
        btn_switch.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        layout.addWidget(self.reg_user_input)
        layout.addWidget(self.reg_pass_input)
        layout.addSpacing(20)
        layout.addWidget(btn_register)
        layout.addWidget(btn_switch)
        
        return widget

    def handle_login(self):
        user = self.login_user_input.text().strip()
        pwd = self.login_pass_input.text()
        
        success, msg = self.user_system.login(user, pwd)
        if success:
            self.login_successful.emit(user)
        else:
            QMessageBox.warning(self, "Access Denied", msg)

    def handle_register(self):
        user = self.reg_user_input.text().strip()
        pwd = self.reg_pass_input.text()
        
        success, msg = self.user_system.register(user, pwd)
        if success:
            QMessageBox.information(self, "Profile Initialized", "You can now log in.")
            self.stack.setCurrentIndex(0)
            self.login_user_input.setText(user)
            self.login_pass_input.clear()
        else:
            QMessageBox.warning(self, "Registration Failed", msg)

    # Allow Enter key to trigger action
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if self.stack.currentIndex() == 0:
                self.handle_login()
            else:
                self.handle_register()
