from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt, Signal

class Sidebar(QWidget):
    page_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.setFixedWidth(240)
        self.setStyleSheet("background-color: #1e293b; border-right: 1px solid #334155;")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title area
        title_area = QWidget()
        title_area.setStyleSheet("border-bottom: 1px solid #334155;")
        title_layout = QVBoxLayout(title_area)
        title = QLabel("CyberToolkit v3.1")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #10b981; border: none; padding: 10px;")
        title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title)
        main_layout.addWidget(title_area)
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        self.scroll_content = QWidget()
        self.layout = QVBoxLayout(self.scroll_content)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)
        
        self.buttons = {}
        
        # We categorize them with Labels for better UX!
        self._add_category_label("AĞ VE YÖNETİM MERKEZİ")
        self._add_button("Gösterge Paneli")
        self._add_button("Port Tarayıcı")
        self._add_button("Ağ Tarayıcı")
        self._add_button("Canlı Bağlantılar")
        self._add_button("Raporlar")
        self._add_button("Tarama Geçmişi")
        self._add_button("Ayarlar")
        
        self._add_category_label("KİŞİSEL GÜVENLİK (DEFANS)")
        self._add_button("Hosts Kalkanı")
        self._add_button("Zararlı İşlem Avcısı")
        self._add_button("Kamera/Mik. Bekçisi")
        self._add_button("Siber Kapan (Tuzak)")
        self._add_button("USB Aşısı")
        self._add_button("Gelişmiş Zırh")
        
        self._add_category_label("KRİPTOGRAFİ & ŞİFRELEME")
        self._add_button("Hash Oluşturucu")
        self._add_button("Base64 Format")
        self._add_button("Metin Şifreleyici")
        self._add_button("Şifre Üretici")
        self._add_button("Şifre Analizcisi")
        
        self._add_category_label("SİSTEM ARAÇLARI")
        self._add_button("Ping Aracı")
        self._add_button("MAC Denetleyici")
        self._add_button("URL Kodlayıcı")
        self._add_button("Alt Ağ (Subnet)")
        self._add_button("DNS Sorgusu")
        self._add_button("Sistem Bilgisi")
        
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.scroll.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll)
        
        # Logout
        logout_area = QWidget()
        logout_layout = QVBoxLayout(logout_area)
        logout_layout.setContentsMargins(10, 10, 10, 10)
        self.logout_btn = QPushButton("Çıkış Yap")
        self.logout_btn.setStyleSheet("""
            QPushButton { background-color: #ef4444; color: white; border: none; border-radius: 6px; padding: 12px; font-weight: bold; } 
            QPushButton:hover { background-color: #dc2626; }
        """)
        logout_layout.addWidget(self.logout_btn)
        main_layout.addWidget(logout_area)
        
        self.active_page = None

    def _add_category_label(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet("font-size: 11px; font-weight: bold; color: #94a3b8; margin-top: 15px; margin-bottom: 5px; border: none;")
        self.layout.addWidget(lbl)

    def _add_button(self, page_name):
        btn = QPushButton(page_name)
        btn.setStyleSheet(self._get_normal_style())
        btn.clicked.connect(lambda checked=False, p=page_name: self.on_btn_clicked(p))
        self.layout.addWidget(btn)
        self.buttons[page_name] = btn

    def _get_normal_style(self):
        return """
            QPushButton { text-align: left; padding: 10px; border: none; background-color: transparent; color: #cbd5e1; font-size: 13px; font-weight: bold; } 
            QPushButton:hover { color: #ffffff; background-color: #334155; border-radius: 6px; }
        """

    def _get_active_style(self):
        return """
            QPushButton { text-align: left; padding: 10px; border: none; background-color: #3b82f6; color: #ffffff; font-size: 13px; font-weight: bold; border-radius: 6px; }
        """

    def on_btn_clicked(self, page_name):
        self._highlight_button(page_name)
        self.page_changed.emit(page_name)

    def _highlight_button(self, page_name):
        if self.active_page and self.active_page in self.buttons:
            self.buttons[self.active_page].setStyleSheet(self._get_normal_style())
            
        self.active_page = page_name
        self.buttons[page_name].setStyleSheet(self._get_active_style())
