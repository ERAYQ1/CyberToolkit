import winreg

class USBVaccine:
    def __init__(self):
        self.reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer"

    def check_status(self):
        """Returns True if AutoRun is fully disabled (0xFF)."""
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.reg_path, 0, winreg.KEY_READ)
            val, _ = winreg.QueryValueEx(key, "NoDriveTypeAutoRun")
            winreg.CloseKey(key)
            return val == 255 # 0xFF
        except FileNotFoundError:
            return False
        except PermissionError:
            return -1

    def apply_vaccine(self):
        """Disables AutoRun for all drives."""
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.reg_path, 0, winreg.KEY_SET_VALUE | winreg.KEY_READ)
        except FileNotFoundError:
            try:
                key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, self.reg_path)
            except PermissionError:
                return False, "Yönetici izni reddedildi."
        except PermissionError:
            return False, "Yönetici izni reddedildi. Lütfen uygulamayı sağ tıklayıp Yönetici Olarak Çalıştırın."

        try:
            winreg.SetValueEx(key, "NoDriveTypeAutoRun", 0, winreg.REG_DWORD, 255) # 0xFF disables all
            winreg.CloseKey(key)
            return True, "Aşı başarıyla uygulandı. USB'lerden otomatik virüs bulaşması engellendi."
        except Exception as e:
            return False, f"Hata: {str(e)}"

    def remove_vaccine(self):
        """Restores default Windows AutoRun behavior (usually 0x91)."""
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.reg_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "NoDriveTypeAutoRun", 0, winreg.REG_DWORD, 145) # 0x91 default
            winreg.CloseKey(key)
            return True, "Aşı kaldırıldı. Orijinal Windows ayarlarına dönüldü."
        except PermissionError:
            return False, "Yönetici izni reddedildi."
        except Exception as e:
            return False, f"Hata: {str(e)}"
