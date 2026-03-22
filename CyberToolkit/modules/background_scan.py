import threading
import time
from utils.database import db


class BackgroundScanSystem:
    def __init__(self):
        self._is_running = False
        self._interval = 3600

    def start_auto_scan(self, interval_minutes=60):
        self._interval = interval_minutes * 60
        self._is_running = True
        t = threading.Thread(target=self._loop, daemon=True)
        t.start()

    def stop_auto_scan(self):
        self._is_running = False

    def _loop(self):
        while self._is_running:
            self._run_scan()
            for _ in range(self._interval):
                if not self._is_running:
                    return
                time.sleep(1)

    def _run_scan(self):
        """Runs a lightweight background network scan."""
        try:
            from modules.network_scanner import NetworkScanner
            scanner = NetworkScanner()
            scanner.start_scan()
            db.add_history("Background Auto Scan", {"status": "completed"})
        except Exception:
            pass


bg_scanner = BackgroundScanSystem()
