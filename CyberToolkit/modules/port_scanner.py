import socket
import threading
from PySide6.QtCore import QObject, Signal

class PortScanner(QObject):
    progress = Signal(int)
    result_found = Signal(str, int, str) # ip, port, description
    finished = Signal()

    def __init__(self):
        super().__init__()
        self._is_running = False
        self._threads = []
        self._queue = []
        
        # Common ports
        self.common_ports = {
            21: "FTP",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            143: "IMAP",
            443: "HTTPS",
            445: "SMB",
            3306: "MySQL",
            3389: "RDP",
            8080: "HTTP-Proxy"
        }

    def start_scan(self, ip, start_port, end_port, thread_count=100):
        self._is_running = True
        self._queue = list(range(start_port, end_port + 1))
        self.total_ports = len(self._queue)
        self.scanned_ports = 0
        
        self._threads = []
        for _ in range(thread_count):
            t = threading.Thread(target=self._worker, args=(ip,))
            t.daemon = True
            t.start()
            self._threads.append(t)
            
        # Thread to wait for completion
        threading.Thread(target=self._wait_for_completion, daemon=True).start()

    def stop_scan(self):
        self._is_running = False

    def _worker(self, ip):
        while self._is_running and self._queue:
            try:
                port = self._queue.pop(0)
            except IndexError:
                break
                
            self._scan_port(ip, port)
            
            self.scanned_ports += 1
            if self.total_ports > 0:
                prog = int((self.scanned_ports / self.total_ports) * 100)
                self.progress.emit(prog)

    def _scan_port(self, ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        try:
            result = sock.connect_ex((ip, port))
            if result == 0:
                service = self.common_ports.get(port, "Unknown Service")
                self.result_found.emit(ip, port, service)
        except Exception:
            pass
        finally:
            sock.close()

    def _wait_for_completion(self):
        for t in self._threads:
            t.join()
        if self._is_running:
            self.progress.emit(100)
        self.finished.emit()
        self._is_running = False
