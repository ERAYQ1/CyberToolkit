import psutil
import socket
import threading
import time
from PySide6.QtCore import QObject, Signal

class ConnectionMonitor(QObject):
    connections_updated = Signal(list)

    def __init__(self):
        super().__init__()
        self._is_running = False
        self._interval = 3

    def start_monitor(self, interval=3):
        self._interval = interval
        self._is_running = True
        t = threading.Thread(target=self._monitor_loop)
        t.daemon = True
        t.start()

    def stop_monitor(self):
        self._is_running = False

    def _monitor_loop(self):
        while self._is_running:
            try:
                conns = psutil.net_connections(kind='inet')
                results = []
                for c in conns:
                    # Filter based on status or display all
                    local_ip = c.laddr.ip if c.laddr else ""
                    local_port = c.laddr.port if c.laddr else ""
                    remote_ip = c.raddr.ip if c.raddr else ""
                    remote_port = c.raddr.port if c.raddr else ""
                    status = c.status
                    pid = c.pid
                    name = ""
                    if pid:
                        try:
                            name = psutil.Process(pid).name()
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            pass
                    
                    # Basic rule: highlight if connection to unusual remote port or status is established but name unknown
                    suspicious = False
                    if status == "ESTABLISHED" and remote_port not in [80, 443, 22, 53] and remote_port != "":
                        suspicious = True
                    
                    results.append({
                        "local": f"{local_ip}:{local_port}",
                        "remote": f"{remote_ip}:{remote_port}",
                        "status": status,
                        "process": name,
                        "pid": pid,
                        "suspicious": suspicious
                    })
                
                self.connections_updated.emit(results)
            except Exception as e:
                pass
                
            time.sleep(self._interval)
