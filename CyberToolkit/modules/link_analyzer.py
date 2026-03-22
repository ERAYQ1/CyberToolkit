import urllib.request
import urllib.error
import urllib.parse
from PySide6.QtCore import QObject, Signal

class LinkAnalyzer(QObject):
    result_found = Signal(dict)

    def analyze(self, url: str):
        import threading
        t = threading.Thread(target=self._worker, args=(url,))
        t.daemon = True
        t.start()

    def _worker(self, url: str):
        if not url.startswith("http"):
            url = "http://" + url
            
        report = {
            "url": url,
            "is_phishing": False,
            "redirects_to": url,
            "server": "Bilinmiyor",
            "warnings": []
        }
        
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc.lower()
        
        # 1. Typosquatting checks
        trusted = ["google", "facebook", "instagram", "twitter", "microsoft", "apple", "paypal", "netflix"]
        for t in trusted:
            if t in domain and domain != t+".com" and domain != "www."+t+".com":
                report["is_phishing"] = True
                report["warnings"].append(f"Oltalama Şüphesi! Orijinal {t.capitalize()} domainini taklit etmeye çalışıyor.")
                break
                
        # 2. Suspicious TLDs or hyphens
        if domain.count("-") > 2:
            report["warnings"].append("Çok fazla tire (-) içeriyor, spam/oltalama sitelerinde yaygındır.")
        if domain.endswith(".xyz") or domain.endswith(".top") or domain.endswith(".stream"):
            report["warnings"].append("Güvenilmez bir uzantı (.xyz, .top vb.) kullanıyor.")
            
        # 3. Request Headers & Redirects
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=5) as resp:
                report["redirects_to"] = resp.geturl()
                if resp.geturl() != url:
                    report["warnings"].append(f"Yönlendirme tespit edildi: {resp.geturl()}")
                
                report["server"] = resp.headers.get('Server', 'Gizlenmiş')
                
                content = resp.read(2048).decode('utf-8', errors='ignore')
                if "login" in content.lower() or "password" in content.lower():
                    report["warnings"].append("Sayfada Şifre/Giriş ekranı tespit edildi. Bilgilerinizi girmeden önce emin olun!")
                    
        except urllib.error.URLError as e:
            report["warnings"].append(f"Siteye ulaşılamadı veya bağlantı koptu: {e.reason}")
        except Exception:
            pass
            
        self.result_found.emit(report)
