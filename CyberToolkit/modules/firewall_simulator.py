import json
import os

class FirewallSimulator:
    """
    Provides a simulated environment for blocking IPs and Ports.
    It doesn't actually alter the OS firewall to prevent system damage,
    but it maintains a strict list and can evaluate if traffic "should" be blocked.
    """
    
    RULES_FILE = "data/firewall_rules.json"

    def __init__(self):
        self._ensure_rules_file()
        self.rules = self.load_rules()

    def _ensure_rules_file(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(self.RULES_FILE):
            with open(self.RULES_FILE, 'w') as f:
                json.dump({"blocked_ips": [], "blocked_ports": []}, f)

    def load_rules(self) -> dict:
        try:
            with open(self.RULES_FILE, 'r') as f:
                return json.load(f)
        except:
            return {"blocked_ips": [], "blocked_ports": []}

    def save_rules(self):
        with open(self.RULES_FILE, 'w') as f:
            json.dump(self.rules, f, indent=4)

    def block_ip(self, ip: str):
        if ip not in self.rules["blocked_ips"]:
            self.rules["blocked_ips"].append(ip)
            self.save_rules()
            return True
        return False

    def unblock_ip(self, ip: str):
        if ip in self.rules["blocked_ips"]:
            self.rules["blocked_ips"].remove(ip)
            self.save_rules()
            return True
        return False

    def block_port(self, port: int):
        if port not in self.rules["blocked_ports"]:
            self.rules["blocked_ports"].append(port)
            self.save_rules()
            return True
        return False

    def unblock_port(self, port: int):
        if port in self.rules["blocked_ports"]:
            self.rules["blocked_ports"].remove(port)
            self.save_rules()
            return True
        return False

    def is_blocked(self, ip: str = None, port: int = None) -> bool:
        if ip and ip in self.rules["blocked_ips"]:
            return True
        if port and port in self.rules["blocked_ports"]:
            return True
        return False
        
    def get_blocked_ips(self):
        return self.rules.get("blocked_ips", [])
    
    def get_blocked_ports(self):
        return self.rules.get("blocked_ports", [])
