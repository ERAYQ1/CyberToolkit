import subprocess
import winreg

class StartupManager:
    def get_startup_items(self):
        """Returns list of programs that run on Windows startup."""
        items = []

        # Registry: HKCU Run
        self._read_reg_key(items, winreg.HKEY_CURRENT_USER,
                           r"Software\Microsoft\Windows\CurrentVersion\Run", "Kullanıcı (Registry)")

        # Registry: HKLM Run
        self._read_reg_key(items, winreg.HKEY_LOCAL_MACHINE,
                           r"Software\Microsoft\Windows\CurrentVersion\Run", "Sistem (Registry)")

        # Task Scheduler common startups
        try:
            res = subprocess.run(
                ["schtasks", "/query", "/fo", "csv", "/nh"],
                capture_output=True, text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            for line in res.stdout.split("\n"):
                parts = line.strip().strip('"').split('","')
                if len(parts) >= 3 and "\\Microsoft\\" not in parts[0]:
                    items.append({
                        "name": parts[0].split("\\")[-1],
                        "path": parts[0],
                        "source": "Zamanlanmış Görev",
                        "status": parts[2] if len(parts) > 2 else ""
                    })
        except Exception:
            pass

        return items

    def _read_reg_key(self, items, hive, path, source):
        try:
            key = winreg.OpenKey(hive, path)
            i = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                    items.append({
                        "name": name,
                        "path": value,
                        "source": source,
                        "status": "Aktif"
                    })
                    i += 1
                except OSError:
                    break
            winreg.CloseKey(key)
        except Exception:
            pass

    def disable_startup_item(self, name):
        """Removes a startup entry from HKCU Run (user-level only for safety)."""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0, winreg.KEY_SET_VALUE
            )
            winreg.DeleteValue(key, name)
            winreg.CloseKey(key)
            return True, f"'{name}' başlangıçtan çıkarıldı."
        except FileNotFoundError:
            return False, f"'{name}' kullanıcı kayıt defterinde bulunamadı."
        except Exception as e:
            return False, f"Hata: {e}"
