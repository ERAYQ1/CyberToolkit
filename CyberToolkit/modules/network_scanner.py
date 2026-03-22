import socket
import threading
import subprocess
import re
import ipaddress
from PySide6.QtCore import QObject, Signal

class NetworkScanner(QObject):
    result_found = Signal(str, str, str) # ip, mac, vendor
    finished = Signal()
    progress = Signal(int)

    def __init__(self):
        super().__init__()
        self._is_running = False

    def start_scan(self):
        self._is_running = True
        t = threading.Thread(target=self._scan_network)
        t.daemon = True
        t.start()

    def stop_scan(self):
        self._is_running = False

    def get_local_ip(self):
        try:
            # A trick to get the primary local IP routing to internet
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "192.168.1.100" # Fallback

    def _ping_host(self, ip):
        if not self._is_running: return
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            sock.connect_ex((str(ip), 135))
            sock.close()
        except:
            pass

    def _scan_network(self):
        try:
            self.progress.emit(10)
            
            local_ip = self.get_local_ip()
            subnet = ".".join(local_ip.split(".")[:-1]) + ".0/24"
            
            self.progress.emit(20)
            
            network = list(ipaddress.IPv4Network(subnet, strict=False).hosts())
            threads = []
            
            for ip in network:
                if not self._is_running: break
                t = threading.Thread(target=self._ping_host, args=(ip,))
                t.daemon = True
                t.start()
                threads.append(t)
                
            self.progress.emit(40)
            
            for t in threads:
                t.join(0.01)
                
            self.progress.emit(60)
            
            if not self._is_running: return
            
            arp_result = subprocess.run(["arp", "-a"], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            lines = arp_result.stdout.split('\n')
            
            self.progress.emit(80)
            
            arp_pattern = re.compile(r"^\s*([0-9\.]+)\s+([0-9a-fA-F\-]+)\s+\w+")
            
            found = set()
            for line in lines:
                if not self._is_running: break
                
                match = arp_pattern.search(line)
                if match:
                    ip = match.group(1)
                    mac = match.group(2).replace("-", ":").upper()
                    
                    if ip.startswith(".".join(local_ip.split(".")[:-1])) and not ip.endswith(".255"):
                        if ip not in found:
                            found.add(ip)
                            vendor = "Cihaz (Ağınızda)"
                            if ip == local_ip:
                                vendor = "Sizin Bilgisayarınız"
                                
                            self.result_found.emit(ip, mac, vendor)
                            
            self.progress.emit(100)
            
        except Exception as e:
            print(f"Ağ Tarama Hatası: {e}")
        finally:
            self.finished.emit()
            self._is_running = False
