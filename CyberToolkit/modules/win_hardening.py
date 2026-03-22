import winreg

class WindowsHardening:
    def __init__(self):
        pass

    def check_uac(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System", 0, winreg.KEY_READ)
            val, _ = winreg.QueryValueEx(key, "EnableLUA")
            winreg.CloseKey(key)
            return val == 1
        except:
            return False
            
    def check_defender(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows Defender", 0, winreg.KEY_READ)
            val, _ = winreg.QueryValueEx(key, "DisableAntiSpyware")
            winreg.CloseKey(key)
            return val == 0 # 0 means NOT disabled -> Defender is ON
        except FileNotFoundError:
            # If key doesn't exist, by default Defender is usually ON in modern windows
            return True
        except PermissionError:
            return -1

    def get_security_report(self):
        report = {
            "UAC_Active": self.check_uac(),
            "Defender_Active": self.check_defender(),
        }
        return report

    def enable_uac(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "EnableLUA", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            return True, "UAC (Hesap Denetimi) açıldı. Bilgisayarınızı yeniden başlatmanız tavsiye edilir."
        except Exception as e:
            return False, f"Hata (Yönetici İzni Yok): {e}"
