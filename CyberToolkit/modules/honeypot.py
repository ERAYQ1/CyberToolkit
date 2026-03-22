import socket
import threading
import time
from PySide6.QtCore import QObject, Signal

class Honeypot(QObject):
    alert_triggered = Signal(str, str, int) # ip, time_str, port

    def __init__(self):
        super().__init__()
        self._is_running = False
        self._sockets = []

    def start_trap(self, ports=[21, 2222, 8080]):
        self._is_running = True
        self._sockets = []
        
        for port in ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind(("0.0.0.0", port))
                s.listen(5)
                s.settimeout(1.0)
                self._sockets.append({"sock": s, "port": port})
                
                t = threading.Thread(target=self._listen_port, args=(s, port))
                t.daemon = True
                t.start()
            except Exception as e:
                print(f"Honeypot bind error for port {port}: {e}")

    def stop_trap(self):
        self._is_running = False
        time.sleep(1) # wait for threads to timeout
        for entry in self._sockets:
            try:
                entry["sock"].close()
            except:
                pass
        self._sockets = []

    def _listen_port(self, s, port):
        while self._is_running:
            try:
                conn, addr = s.accept()
                ip = addr[0]
                self.alert_triggered.emit(ip, time.strftime("%H:%M:%S"), port)
                
                # Send a fake banner
                try:
                    conn.sendall(b"220 Microsoft FTP Service\r\nLogin:\r\n")
                    # just hold for a sec then close
                    time.sleep(2)
                except:
                    pass
                finally:
                    conn.close()
            except socket.timeout:
                continue
            except Exception:
                break
