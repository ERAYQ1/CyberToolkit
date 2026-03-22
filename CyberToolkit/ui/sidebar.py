from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt, Signal
from utils.translations import t


# Internal page IDs mapped to translation keys
PAGE_IDS = [
    ("cat_network", None),
    ("dashboard", "dashboard"),
    ("speed_test", "speed_test"),
    ("net_scanner", "net_scanner"),
    ("port_scanner", "port_scanner"),
    ("cat_defense", None),
    ("malware", "malware"),
    ("hosts_blocker", "hosts_blocker"),
    ("usb_vaccine", "usb_vaccine"),
    ("win_hardening", "win_hardening"),
    ("link_analyzer", "link_analyzer"),
    ("cat_tools", None),
    ("wifi_passwords", "wifi_passwords"),
    ("startup_mgr", "startup_mgr"),
    ("disk_cleaner", "disk_cleaner"),
    ("password_mgr", "password_mgr"),
    ("cat_other", None),
    ("scan_history", "scan_history"),
    ("reports", "reports"),
    ("settings", "settings"),
]


class Sidebar(QWidget):
    page_changed = Signal(str)  # Emits internal page ID

    def __init__(self):
        super().__init__()
        self.setFixedWidth(240)
        self.setStyleSheet("background-color: #1e293b; border-right: 1px solid #334155;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        title_area = QWidget()
        title_area.setStyleSheet("border-bottom: 1px solid #334155;")
        title_layout = QVBoxLayout(title_area)
        self.title_label = QLabel("CyberToolkit")
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #10b981; border: none; padding: 10px;")
        self.title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(self.title_label)
        main_layout.addWidget(title_area)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        self.scroll_content = QWidget()
        self.btn_layout = QVBoxLayout(self.scroll_content)
        self.btn_layout.setContentsMargins(10, 10, 10, 10)
        self.btn_layout.setSpacing(5)

        self.buttons = {}       # page_id -> QPushButton
        self.cat_labels = {}    # cat_key -> QLabel

        for key, page_id in PAGE_IDS:
            if page_id is None:
                self._add_category_label(key)
            else:
                self._add_button(page_id, key)

        self.btn_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.scroll.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll)

        logout_area = QWidget()
        logout_layout = QVBoxLayout(logout_area)
        logout_layout.setContentsMargins(10, 10, 10, 10)
        self.logout_btn = QPushButton(t("close_app"))
        self.logout_btn.setStyleSheet("QPushButton { background-color: #ef4444; color: white; border: none; border-radius: 6px; padding: 12px; font-weight: bold; } QPushButton:hover { background-color: #dc2626; }")
        logout_layout.addWidget(self.logout_btn)
        main_layout.addWidget(logout_area)

        self.active_page = None

    def _add_category_label(self, key):
        lbl = QLabel(t(key))
        lbl.setStyleSheet("font-size: 11px; font-weight: bold; color: #94a3b8; margin-top: 15px; margin-bottom: 5px; border: none;")
        self.btn_layout.addWidget(lbl)
        self.cat_labels[key] = lbl

    def _add_button(self, page_id, trans_key):
        btn = QPushButton(t(trans_key))
        btn.setStyleSheet(self._get_normal_style())
        btn.clicked.connect(lambda checked=False, pid=page_id: self.on_btn_clicked(pid))
        self.btn_layout.addWidget(btn)
        self.buttons[page_id] = btn

    def retranslate(self):
        """Re-apply all translated labels after language change."""
        for key, page_id in PAGE_IDS:
            if page_id is None:
                if key in self.cat_labels:
                    self.cat_labels[key].setText(t(key))
            else:
                if page_id in self.buttons:
                    self.buttons[page_id].setText(t(page_id))
        self.logout_btn.setText(t("close_app"))

    def _get_normal_style(self):
        return "QPushButton { text-align: left; padding: 10px; border: none; background-color: transparent; color: #cbd5e1; font-size: 13px; font-weight: bold; } QPushButton:hover { color: #ffffff; background-color: #334155; border-radius: 6px; }"

    def _get_active_style(self):
        return "QPushButton { text-align: left; padding: 10px; border: none; background-color: #3b82f6; color: #ffffff; font-size: 13px; font-weight: bold; border-radius: 6px; }"

    def on_btn_clicked(self, page_id):
        self._highlight_button(page_id)
        self.page_changed.emit(page_id)

    def _highlight_button(self, page_id):
        if self.active_page and self.active_page in self.buttons:
            self.buttons[self.active_page].setStyleSheet(self._get_normal_style())
        self.active_page = page_id
        if page_id in self.buttons:
            self.buttons[page_id].setStyleSheet(self._get_active_style())
