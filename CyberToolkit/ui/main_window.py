from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt, QTimer
from .themes import get_theme
from .sidebar import Sidebar
from ui.pages import *
from utils.database import db
from utils.translations import t, set_language, get_language
from modules.background_scan import bg_scanner


class LoginWindow(QWidget):
    def __init__(self, apply_theme_func, on_success):
        super().__init__()
        self.apply_theme_func = apply_theme_func
        self.on_success = on_success

        settings = db.get_settings()
        theme = settings.get("theme", "Dark Hacker")
        lang = settings.get("language", "tr")
        set_language(lang)

        self.setStyleSheet(get_theme(theme))
        self.setFixedSize(400, 380)
        self.setWindowTitle(t("login_title"))

        from PySide6.QtWidgets import QVBoxLayout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel(t("app_title"))
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #10b981; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.input_usr = QLineEdit()
        self.input_usr.setPlaceholderText(t("username"))
        layout.addWidget(self.input_usr)

        self.input_pwd = QLineEdit()
        self.input_pwd.setPlaceholderText(t("password"))
        self.input_pwd.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.input_pwd)

        btn_login = QPushButton(t("login_btn"))
        btn_login.clicked.connect(self.do_login)
        layout.addWidget(btn_login)

        btn_reg = QPushButton(t("register_btn"))
        btn_reg.clicked.connect(self.do_register)
        layout.addWidget(btn_reg)

        lbl_warn = QLabel(t("login_warn"))
        lbl_warn.setStyleSheet("color: #ef4444; font-size: 10px; margin-top: 15px; font-weight: bold;")
        lbl_warn.setWordWrap(True)
        lbl_warn.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_warn)

    def do_login(self):
        usr = self.input_usr.text().strip()
        pwd = self.input_pwd.text().strip()
        if not usr or not pwd:
            return
        saved_pwd = db.get_user(usr)
        if saved_pwd == pwd:
            self.on_success(usr)
            self.close()
        else:
            QMessageBox.warning(self, t("error"), t("login_error"))

    def do_register(self):
        usr = self.input_usr.text().strip()
        pwd = self.input_pwd.text().strip()
        if not usr or not pwd:
            return
        if db.get_user(usr):
            QMessageBox.warning(self, t("error"), t("user_exists"))
            return
        db.save_user(usr, pwd)
        QMessageBox.information(self, t("success"), t("register_ok"))


class MainWindow(QMainWindow):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.setWindowTitle("CyberToolkit")
        self.resize(1100, 700)

        theme = db.get_settings().get("theme", "Dark Hacker")
        self.setStyleSheet(get_theme(theme))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = Sidebar()
        self.sidebar.page_changed.connect(self._switch_page)
        main_layout.addWidget(self.sidebar)

        self.stacked = QStackedWidget()
        main_layout.addWidget(self.stacked)

        # Map internal IDs to page widgets
        self.tools = {
            "dashboard":      DashboardPage(),
            "speed_test":     SpeedTestPage(),
            "net_scanner":    NetworkScannerPage(),
            "port_scanner":   PortScannerPage(),
            "malware":        MalwareScannerPage(),
            "hosts_blocker":  HostsBlockerPage(),
            "usb_vaccine":    USBVaccinePage(),
            "win_hardening":  WindowsHardeningPage(),
            "link_analyzer":  LinkAnalyzerPage(),
            "wifi_passwords": WiFiPasswordsPage(),
            "startup_mgr":    StartupManagerPage(),
            "disk_cleaner":   DiskCleanerPage(),
            "password_mgr":   PasswordManagerPage(),
            "scan_history":   ScanHistoryPage(),
            "reports":        ReportsPage(),
            "settings":       SettingsPage()
        }

        self.tools["settings"].theme_changed.connect(self._apply_theme)
        self.tools["settings"].language_changed.connect(self._apply_language)

        for page_obj in self.tools.values():
            self.stacked.addWidget(page_obj)

        self.sidebar.on_btn_clicked("dashboard")
        self.sidebar.logout_btn.clicked.connect(self.logout)

        bg_scanner.start_auto_scan(interval_minutes=60)

        self._update_dashboard_stats()
        self.dash_timer = QTimer(self)
        self.dash_timer.timeout.connect(self._update_dashboard_stats)
        self.dash_timer.start(5000)

    def _switch_page(self, page_id):
        if page_id in self.tools:
            if page_id == "scan_history":
                self.tools["scan_history"].load_history()
            self.stacked.setCurrentWidget(self.tools[page_id])

    def _apply_theme(self, theme_name):
        self.setStyleSheet(get_theme(theme_name))
        self.sidebar.on_btn_clicked(self.sidebar.active_page)

    def _apply_language(self, lang_code):
        set_language(lang_code)
        self.sidebar.retranslate()
        # Re-translate pages that support it
        for page in self.tools.values():
            if hasattr(page, "retranslate"):
                page.retranslate()

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
            self.tools["dashboard"].update_stats(devices, ports, conns, score)
        except Exception:
            pass

    def logout(self):
        bg_scanner.stop_auto_scan()
        self.close()
