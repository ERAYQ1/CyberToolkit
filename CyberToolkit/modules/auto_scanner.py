from PySide6.QtCore import QThread, Signal

class AutoScannerWorker(QThread):
    """
    A background thread to trigger automatic lightweight scans at defined intervals.
    Instead of actually doing the work, it emits a signal to tell the main app to start a scan.
    """
    trigger_scan = Signal(str)

    def __init__(self, interval_minutes: int):
        super().__init__()
        self.interval_sec = interval_minutes * 60
        self.is_running = True

    def run(self):
        # We don't want to scan immediately upon start, wait for interval first
        while self.is_running:
            for _ in range(self.interval_sec):
                if not self.is_running:
                    return
                QThread.sleep(1)
            
            # Emit signal to notify main window to perform a silent auto-scan
            if self.is_running:
                self.trigger_scan.emit('AUTO_SCAN')

    def stop(self):
        self.is_running = False
