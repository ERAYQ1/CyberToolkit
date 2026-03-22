from ui.pages.dashboard import DashboardPage
from ui.pages.port_scanner import PortScannerPage
from ui.pages.network_scanner import NetworkScannerPage
from ui.pages.password_analyzer import PasswordAnalyzerPage
from ui.pages.connection_monitor import ConnectionMonitorPage
from ui.pages.scan_history import ScanHistoryPage
from ui.pages.reports import ReportsPage
from ui.pages.settings import SettingsPage

from ui.pages.hash_generator import HashGeneratorPage
from ui.pages.base64_tool import Base64ToolPage
from ui.pages.ping_tool import PingToolPage
from ui.pages.mac_tool import MacToolPage
from ui.pages.url_tool import UrlToolPage
from ui.pages.subnet_calculator import SubnetCalculatorPage
from ui.pages.dns_lookup import DnsLookupPage
from ui.pages.system_info import SystemInfoPage
from ui.pages.text_encryptor import TextEncryptorPage
from ui.pages.password_generator import PasswordGeneratorPage

# New Security Modules
from ui.pages.hosts_blocker import HostsBlockerPage
from ui.pages.malware_scanner import MalwareScannerPage
from ui.pages.cam_mic_monitor import CamMicMonitorPage
from ui.pages.honeypot import HoneypotPage
from ui.pages.usb_vaccine import USBVaccinePage
from ui.pages.win_hardening import WindowsHardeningPage

__all__ = [
    "DashboardPage", "PortScannerPage", "NetworkScannerPage", "PasswordAnalyzerPage",
    "ConnectionMonitorPage", "ScanHistoryPage", "ReportsPage", "SettingsPage",
    "HashGeneratorPage", "Base64ToolPage", "PingToolPage", "MacToolPage",
    "UrlToolPage", "SubnetCalculatorPage", "DnsLookupPage", "SystemInfoPage",
    "TextEncryptorPage", "PasswordGeneratorPage",
    "HostsBlockerPage", "MalwareScannerPage", "CamMicMonitorPage", "HoneypotPage",
    "USBVaccinePage", "WindowsHardeningPage"
]
