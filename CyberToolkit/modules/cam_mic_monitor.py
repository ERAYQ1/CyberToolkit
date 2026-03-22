import time
import threading
import winreg
from PySide6.QtCore import QObject, Signal

class DeviceMonitor(QObject):
    alert_triggered = Signal(str, str, str) # device_type, exe_name, time_str

    def __init__(self):
        super().__init__()
        self._is_running = False
        self._thread = None

    def start_monitor(self):
        if self._is_running: return
        self._is_running = True
        self._thread = threading.Thread(target=self._monitor_loop)
        self._thread.daemon = True
        self._thread.start()

    def stop_monitor(self):
        self._is_running = False

    def _check_reg_key(self, device):
        # device is 'webcam' or 'microphone'
        path = rf"Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\{device}\NonPackaged"
        active_apps = []
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path)
            for i in range(100):
                try:
                    sub_key_name = winreg.EnumKey(key, i)
                    sub_key = winreg.OpenKey(key, sub_key_name)
                    # LastUsedTimeStop == 0 means currently using
                    val, _ = winreg.QueryValueEx(sub_key, "LastUsedTimeStop")
                    if val == 0:
                        active_apps.append(sub_key_name.replace('#', '\\').split('\\')[-1])
                    winreg.CloseKey(sub_key)
                except OSError:
                    break
            winreg.CloseKey(key)
        except FileNotFoundError:
            pass
        return active_apps

    def _monitor_loop(self):
        # We track state to avoid spamming alerts
        active_cams = set()
        active_mics = set()
        
        while self._is_running:
            time.sleep(3)
            
            curr_cams = set(self._check_reg_key("webcam"))
            for app in curr_cams:
                if app not in active_cams:
                    self.alert_triggered.emit("Kamera", app, time.strftime("%H:%M:%S"))
            active_cams = curr_cams
            
            curr_mics = set(self._check_reg_key("microphone"))
            for app in curr_mics:
                if app not in active_mics:
                    self.alert_triggered.emit("Mikrofon", app, time.strftime("%H:%M:%S"))
            active_mics = curr_mics
