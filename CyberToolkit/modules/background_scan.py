import threading
import time
from .port_scanner import PortScanner
from .network_scanner import NetworkScanner
from utils.database import db

class BackgroundScanSystem:
    def __init__(self):
        self._is_running = False
        self._interval = 60 * 60 # Default 1 hour
        self.port_scanner = PortScanner()
        self.network_scanner = NetworkScanner()

    def start_auto_scan(self, interval_minutes=60):
        self._interval = interval_minutes * 60
        self._is_running = True
        t = threading.Thread(target=self._auto_scan_loop)
        t.daemon = True
        t.start()

    def stop_auto_scan(self):
        self._is_running = False

    def _auto_scan_loop(self):
        while self._is_running:
            # Perform a background network scan
            self._run_network_scan()
            
            # Wait for interval manually to allow interruption
            for _ in range(self._interval):
                if not self._is_running:
                    break
                time.sleep(1)

    def _run_network_scan(self):
        # We can simulate saving background history
        def on_result(ip, mac, vendor):
            pass # Or log it silently
            
        def on_finished():
            db.add_history("Background Auto Scan", {"status": "completed"})
            
        self.network_scanner.result_found.connect(on_result)
        self.network_scanner.finished.connect(on_finished)
        
        self.network_scanner.start_scan()

bg_scanner = BackgroundScanSystem()
