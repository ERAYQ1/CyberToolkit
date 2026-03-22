import os

HOSTS_PATH = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'System32', 'drivers', 'etc', 'hosts')

# A generic list of known telemetry and ad servers for demonstration
BLOCKLIST = [
    "0.0.0.0 adservice.google.com",
    "0.0.0.0 v10.events.data.microsoft.com",
    "0.0.0.0 telemetry.microsoft.com",
    "0.0.0.0 doubleclick.net",
    "0.0.0.0 google-analytics.com",
    "0.0.0.0 ad.yieldmanager.com"
]

class HostsBlocker:
    def __init__(self):
        pass

    def check_status(self):
        """Returns how many of our protected domains are currently blocked."""
        if not os.path.exists(HOSTS_PATH):
            return 0
            
        try:
            with open(HOSTS_PATH, 'r', encoding='utf-8') as f:
                content = f.read()
            count = sum(1 for line in BLOCKLIST if line in content)
            return count
        except Exception:
            return -1 # Permission Error

    def apply_protection(self):
        """Appends the blocklist to the hosts file."""
        try:
            with open(HOSTS_PATH, 'a', encoding='utf-8') as f:
                f.write("\n# --- CyberToolkit Protection Start ---\n")
                for domain in BLOCKLIST:
                    f.write(f"{domain}\n")
                f.write("# --- CyberToolkit Protection End ---\n")
            return True, "Koruma başarıyla uygulandı."
        except PermissionError:
            return False, "Erişim Reddedildi. Sağ tıklayıp 'Yönetici Olarak Çalıştır'manız gerekir."
        except Exception as e:
            return False, str(e)

    def remove_protection(self):
        """Removes the blocklist from the hosts file."""
        try:
            with open(HOSTS_PATH, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            new_lines = []
            skip = False
            for line in lines:
                if "# --- CyberToolkit Protection Start ---" in line:
                    skip = True
                if not skip:
                    new_lines.append(line)
                if "# --- CyberToolkit Protection End ---" in line:
                    skip = False
                    
            with open(HOSTS_PATH, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            return True, "Koruma başarıyla kaldırıldı."
        except PermissionError:
            return False, "Erişim Reddedildi. Sağ tıklayıp 'Yönetici Olarak Çalıştır'manız gerekir."
        except Exception as e:
            return False, str(e)
