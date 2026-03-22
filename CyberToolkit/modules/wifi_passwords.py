import subprocess

class WiFiPasswords:
    def get_profiles(self):
        """Returns list of saved WiFi network names and their passwords."""
        results = []
        try:
            output = subprocess.run(
                ["netsh", "wlan", "show", "profiles"],
                capture_output=True, text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            profiles = []
            for line in output.stdout.split("\n"):
                if "Tüm Kullanıcı Profili" in line or "All User Profile" in line:
                    name = line.split(":")[-1].strip()
                    if name:
                        profiles.append(name)

            for name in profiles:
                pwd_output = subprocess.run(
                    ["netsh", "wlan", "show", "profile", name, "key=clear"],
                    capture_output=True, text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                password = ""
                auth_type = ""
                for line in pwd_output.stdout.split("\n"):
                    if "Anahtar İçeriği" in line or "Key Content" in line:
                        password = line.split(":")[-1].strip()
                    if "Kimlik Doğrulama" in line or "Authentication" in line:
                        auth_type = line.split(":")[-1].strip()

                results.append({
                    "name": name,
                    "password": password if password else "(Şifre yok veya yetki gerekli)",
                    "auth": auth_type if auth_type else "Bilinmiyor"
                })
        except Exception as e:
            results.append({"name": f"Hata: {e}", "password": "", "auth": ""})

        return results
