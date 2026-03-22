from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt, QTimer
from .themes import get_theme
from .sidebar import Sidebar
from ui.pages import *
from utils.database import db
from modules.background_scan import bg_scanner

# ----------------- LOGIN WINDOW -----------------
class LoginWindow(QWidget):
    def __init__(self, apply_theme_func, on_success):
        super().__init__()
        self.apply_theme_func = apply_theme_func
        self.on_success = on_success
        
        theme = db.get_settings().get("theme", "Dark Hacker")
        self.setStyleSheet(get_theme(theme))
        self.setFixedSize(400, 350)
        self.setWindowTitle("CyberToolkit v3.1 - Giriş")
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel("CyberToolkit")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #10b981; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        self.input_usr = QLineEdit()
        self.input_usr.setPlaceholderText("Kullanıcı Adı")
        layout.addWidget(self.input_usr)
        
        self.input_pwd = QLineEdit()
        self.input_pwd.setPlaceholderText("Şifre")
        self.input_pwd.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.input_pwd)
        
        btn_login = QPushButton("Giriş Yap")
        btn_login.clicked.connect(self.do_login)
        layout.addWidget(btn_login)
        
        btn_reg = QPushButton("Kayıt Ol")
        btn_reg.clicked.connect(self.do_register)
        layout.addWidget(btn_reg)
        
        lbl_warn = QLabel("YASAL UYARI: Bu yazılım siber güvenlik eğitimleri ve test amacıyla geliştirilmiştir. Kötüye kullanımından, oluşabilecek hasarlardan veya doğacak hukuki süreçlerden geliştirici(ler) kesinlikle sorumlu tutulamaz.")
        lbl_warn.setStyleSheet("color: #ef4444; font-size: 10px; margin-top: 15px; font-weight: bold;")
        lbl_warn.setWordWrap(True)
        lbl_warn.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_warn)
        
    def do_login(self):
        usr = self.input_usr.text().strip()
        pwd = self.input_pwd.text().strip()
        if not usr or not pwd: return
        
        saved_pwd = db.get_user(usr)
        if saved_pwd == pwd:
            self.on_success(usr)
            self.close()
        else:
            QMessageBox.warning(self, "Hata", "Geçersiz kullanıcı adı veya şifre.")
            
    def do_register(self):
        usr = self.input_usr.text().strip()
        pwd = self.input_pwd.text().strip()
        if not usr or not pwd: return
        
        if db.get_user(usr):
            QMessageBox.warning(self, "Hata", "Kullanıcı zaten mevcut.")
            return
            
        db.save_user(usr, pwd)
        QMessageBox.information(self, "Başarılı", "Kayıt başarılı. Şimdi giriş yapabilirsiniz.")

# ----------------- MAIN WINDOW -----------------
class MainWindow(QMainWindow):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.setWindowTitle(f"CyberToolkit v3.1 - Hoşgeldiniz: {current_user}")
        self.resize(1150, 750)
        
        theme = db.get_settings().get("theme", "Dark Hacker")
        self.setStyleSheet(get_theme(theme))
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # We restore QHBoxLayout for Sidebar
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.sidebar = Sidebar()
        self.sidebar.page_changed.connect(self._switch_page)
        main_layout.addWidget(self.sidebar)
        
        self.stacked = QStackedWidget()
        main_layout.addWidget(self.stacked)
        
        # Initialize all tools instances
        self.tools = {
            "Gösterge Paneli": DashboardPage(),
            "Port Tarayıcı": PortScannerPage(),
            "Ağ Tarayıcı": NetworkScannerPage(),
            "Şifre Analizcisi": PasswordAnalyzerPage(),
            "Canlı Bağlantılar": ConnectionMonitorPage(),
            "Raporlar": ReportsPage(),
            "Tarama Geçmişi": ScanHistoryPage(),
            "Ayarlar": SettingsPage(),
            
            "Hosts Kalkanı": HostsBlockerPage(),
            "Zararlı İşlem Avcısı": MalwareScannerPage(),
            "Kamera/Mik. Bekçisi": CamMicMonitorPage(),
            "Siber Kapan (Tuzak)": HoneypotPage(),
            "USB Aşısı": USBVaccinePage(),
            "Gelişmiş Zırh": WindowsHardeningPage(),
            
            "Hash Oluşturucu": HashGeneratorPage(),
            "Base64 Format": Base64ToolPage(),
            "Metin Şifreleyici": TextEncryptorPage(),
            "Şifre Üretici": PasswordGeneratorPage(),
            
            "Ping Aracı": PingToolPage(),
            "MAC Denetleyici": MacToolPage(),
            "URL Kodlayıcı": UrlToolPage(),
            "Alt Ağ (Subnet)": SubnetCalculatorPage(),
            "DNS Sorgusu": DnsLookupPage(),
            "Sistem Bilgisi": SystemInfoPage()
        }
        
        self.tools["Ayarlar"].theme_changed.connect(self._apply_theme)
        
        for name, page_obj in self.tools.items():
            self.stacked.addWidget(page_obj)
            
        self.sidebar.on_btn_clicked("Gösterge Paneli")
        self.sidebar.logout_btn.clicked.connect(self.logout)
        
        bg_scanner.start_auto_scan(interval_minutes=60)
        
        self._update_dashboard_stats()
        self.dash_timer = QTimer(self)
        self.dash_timer.timeout.connect(self._update_dashboard_stats)
        self.dash_timer.start(5000)

    def _switch_page(self, page_name):
        if page_name in self.tools:
            if page_name == "Tarama Geçmişi":
                self.tools["Tarama Geçmişi"].load_history()
            self.stacked.setCurrentWidget(self.tools[page_name])

    def _apply_theme(self, theme_name):
        self.setStyleSheet(get_theme(theme_name))
        self.sidebar.on_btn_clicked(self.sidebar.active_page)

    def _update_dashboard_stats(self):
        try:
            import psutil
            conns = len(psutil.net_connections(kind='inet'))
            devices = 0
            ports = 0
            hist = db.get_history()
            for h in reversed(hist):
                if h["type"] == "Network Scan" and devices == 0:
                    devices = h["details"].get("devices_found", 0)
                if h["type"] == "Port Scan" and ports == 0:
                    ports = h["details"].get("open_ports_count", 0)
            score = max(0, 100 - (ports * 5) - (conns // 10))
            self.tools["Gösterge Paneli"].update_stats(devices, ports, conns, score)
        except Exception:
            pass

    def logout(self):
        bg_scanner.stop_auto_scan()
        self.close()
