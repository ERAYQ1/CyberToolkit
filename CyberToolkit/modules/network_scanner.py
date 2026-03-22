import socket
import threading
import subprocess
import re
import ipaddress
import time
from PySide6.QtCore import QObject, Signal

class NetworkScanner(QObject):
    result_found = Signal(str, str, str, str, float)  # ip, mac, vendor, hostname, response_ms
    finished = Signal(int)  # total found count
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
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "192.168.1.100"

    def _resolve_hostname(self, ip):
        try:
            name, _, _ = socket.gethostbyaddr(ip)
            return name
        except Exception:
            return ""

    def _ping_host(self, ip):
        if not self._is_running:
            return
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.15)
            sock.connect_ex((str(ip), 135))
            sock.close()
        except Exception:
            pass

    def _measure_response(self, ip):
        try:
            start = time.perf_counter()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            sock.connect_ex((str(ip), 135))
            sock.close()
            return round((time.perf_counter() - start) * 1000, 1)
        except Exception:
            return -1.0

    def _guess_device_type(self, ip, hostname, local_ip):
        if ip == local_ip:
            return "💻 Bu Bilgisayar"

        hn = hostname.lower()
        last_octet = int(ip.split(".")[-1])

        if last_octet == 1:
            return "📡 Modem / Router"
        if "android" in hn or "galaxy" in hn or "xiaomi" in hn or "redmi" in hn or "huawei" in hn:
            return "📱 Telefon (Android)"
        if "iphone" in hn or "ipad" in hn:
            return "📱 Apple Cihaz"
        if "desktop" in hn or "pc" in hn or "laptop" in hn:
            return "💻 Bilgisayar"
        if "tv" in hn or "smart" in hn or "cast" in hn or "roku" in hn:
            return "📺 Akıllı TV"
        if "printer" in hn or "epson" in hn or "hp" in hn or "canon" in hn:
            return "🖨️ Yazıcı"
        if "cam" in hn or "nvr" in hn or "hikvision" in hn:
            return "📹 Güvenlik Kamerası"

        return "❓ Bilinmeyen Cihaz"

    def _scan_network(self):
        try:
            self.progress.emit(5)

            local_ip = self.get_local_ip()
            subnet = ".".join(local_ip.split(".")[:-1]) + ".0/24"

            self.progress.emit(10)

            network = list(ipaddress.IPv4Network(subnet, strict=False).hosts())
            threads = []

            for ip in network:
                if not self._is_running:
                    break
                t = threading.Thread(target=self._ping_host, args=(ip,))
                t.daemon = True
                t.start()
                threads.append(t)

            self.progress.emit(30)

            for t in threads:
                t.join(0.02)

            self.progress.emit(50)

            if not self._is_running:
                return

            arp_result = subprocess.run(
                ["arp", "-a"], capture_output=True, text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            lines = arp_result.stdout.split('\n')

            self.progress.emit(60)

            arp_pattern = re.compile(r"^\s*([0-9\.]+)\s+([0-9a-fA-F\-]+)\s+\w+")

            found = set()
            total = 0
            subnet_prefix = ".".join(local_ip.split(".")[:-1])

            for line in lines:
                if not self._is_running:
                    break

                match = arp_pattern.search(line)
                if match:
                    ip = match.group(1)
                    mac = match.group(2).replace("-", ":").upper()

                    if ip.startswith(subnet_prefix) and not ip.endswith(".255"):
                        if ip not in found:
                            found.add(ip)

                            hostname = self._resolve_hostname(ip)
                            response_ms = self._measure_response(ip)
                            device_type = self._guess_device_type(ip, hostname, local_ip)

                            self.result_found.emit(ip, mac, device_type, hostname, response_ms)
                            total += 1

            self.progress.emit(100)

        except Exception as e:
            print(f"Ağ Tarama Hatası: {e}")
        finally:
            self.finished.emit(total if 'total' in dir() else 0)
            self._is_running = False
