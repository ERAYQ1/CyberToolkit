from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt, Signal

class Sidebar(QWidget):
    page_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.setFixedWidth(230)
        self.setStyleSheet("background-color: #1e293b; border-right: 1px solid #334155;")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title area
        title_area = QWidget()
        title_layout = QVBoxLayout(title_area)
        title = QLabel("CyberToolkit")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #10b981; border: none; padding: 10px;")
        title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title)
        main_layout.addWidget(title_area)
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none; background-color: transparent;")
        
        self.scroll_content = QWidget()
        self.layout = QVBoxLayout(self.scroll_content)
        self.layout.setContentsMargins(10, 0, 10, 0)
        self.layout.setSpacing(5)
        
        self.buttons = {}
        
        # Updated pages list including 10 new and old components in Turkish
        pages = [
            "Gösterge Paneli", "Port Tarayıcı", "Ağ Tarayıcı (ARP)", 
            "Şifre Analizcisi", "Canlı Bağlantılar", 
            "Hash Oluşturucu", "Base64 Dönüştürücü", "Ping Aracı", 
            "MAC Denetleyici", "URL Kodlayıcı", "Alt Ağ Hesaplayıcı",
            "DNS Sorgu", "Sistem Bilgisi", "Metin Şifreleyici",
            "Güvenli Şifre Oluş.",
            "Tarama Geçmişi", "Raporlar", "Ayarlar"
        ]
        
        for page in pages:
            btn = QPushButton(page)
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 10px;
                    border: none;
                    background-color: transparent;
                    color: #94a3b8;
                    font-size: 14px;
                }
                QPushButton:hover {
                    color: #ffffff;
                    background-color: #334155;
                    border-radius: 5px;
                }
            """)
            btn.clicked.connect(lambda checked=False, p=page: self.on_btn_clicked(p))
            self.layout.addWidget(btn)
            self.buttons[page] = btn
            
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.scroll.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll)
        
        # Logout button area
        logout_area = QWidget()
        logout_layout = QVBoxLayout(logout_area)
        logout_layout.setContentsMargins(10, 10, 10, 10)
        self.logout_btn = QPushButton("Çıkış Yap (Logout)")
        self.logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        logout_layout.addWidget(self.logout_btn)
        main_layout.addWidget(logout_area)
        
        self.active_page = None
        
    def on_btn_clicked(self, page_name):
        self._highlight_button(page_name)
        self.page_changed.emit(page_name)

    def _highlight_button(self, page_name):
        if self.active_page and self.active_page in self.buttons:
            self.buttons[self.active_page].setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 10px;
                    border: none;
                    background-color: transparent;
                    color: #94a3b8;
                    font-size: 14px;
                }
                QPushButton:hover {
                    color: #ffffff;
                    background-color: #334155;
                    border-radius: 5px;
                }
            """)
            
        self.active_page = page_name
        self.buttons[page_name].setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 10px;
                border: none;
                background-color: #3b82f6;
                color: #ffffff;
                font-size: 14px;
                border-radius: 5px;
            }
        """)
