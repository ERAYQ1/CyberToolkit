# 🛡️ CyberToolkit v3.1

> **⚠️ LEGAL DISCLAIMER / YASAL UYARI:**  
> *This tool is meant strictly for educational and administrative purposes on systems you own or have explicit permission to audit. Any illegal or unauthorized usage is strongly prohibited. The developer(s) assume no liability and are not responsible for any misuse, damage, or legal consequences caused by this software.*  
> 
> *Bu araç kesinlikle siber güvenlik eğitimleri, sistem testleri ve izinli olduğunuz ağlarda zafiyet analizi yapmak amacıyla geliştirilmiştir. Yasadışı, zarar verici veya izinsiz herhangi bir kullanımı kesinlikle yasaktır. Bu yazılımın kullanımından doğabilecek her türlü kötüye kullanım, veri kaybı, hasar veya hukuki sonuçtan yazılımı kullanan kişi sorumludur, geliştirici(ler) kesinlikle sorumlu tutulamaz.*

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-GUI-green.svg)
![Security](https://img.shields.io/badge/Security-Localizer-red.svg)
![License](https://img.shields.io/badge/License-MIT-purple.svg)

*(🇹🇷 Türkçe açıklamalar aşağıdadır / Turkish description is below)*

**CyberToolkit v3.1** is the ultimate, universally offline, entirely native desktop cybersecurity utility suite. Featuring **24 advanced modules**, it requires zero external packet-sniffing drivers (such as WinPcap or Npcap). Relying entirely on native Python sockets and Windows APIs, CyberToolkit provides both offensive reconnaissance tools and defensive Local Security features all packed inside a beautifully categorized Sidebar interface.

### 🌟 English Features (24 Modules)
- **Active Defense (New in v3.1)**: Hosts Blocker (Ad/Telemetry prevention), Malware Scanner (Hidden process heuristics), Cam/Mic Monitor (Surveillance alerts), Honeypot (Local Network Trap), USB Vaccine (AutoRun Blocker), and Windows Hardening.
- **Network & Recon**: One-Click Network Discovery (Native ARP array), Multi-threaded Port Scanner, Live Connection Tracker.
- **Cryptography**: Hash Generator (MD5, SHA variants), Base64 Encoder/Decoder, Advanced Key-XOR Text Encryptor.
- **System Utilities**: High-performance ICMP Ping Tool, IPv4 Subnet Calculator, DNS & Reverse DNS Lookup, MAC Address Forge/Validator, Detailed System Hardware Info.
- **Security Assessors**: Password Strength Calculator (with Time-to-Crack), Secure Customizable Password Generator, URL Decoder/Encoder.
- **Reporting Engine**: Exports all network histories & stats to **PDF** or **CSV** formats for professional auditing.

### 🚀 Installation (English)
1. Ensure Python 3.10+ is installed on your Windows system.
2. Clone this repository and install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```
*(Note: Certain tools like Hosts Blocker and USB Vaccine require Administrative Privileges. Launching cmd as Administrator is recommended for full feature parity).*

---

## 🇹🇷 Türkçe Açıklamalar

**CyberToolkit v3.1**, internet gereksinimi duymayan, herhangi bir Wi-Fi yakalama kütüphanesine (Npcap vb.) muhtaç olmayan tamamen yerel (native) ve devasa bir masaüstü güvenlik asistanıdır. Yapay zeka barındırmaz, doğrudan makinenizde çalışır. Toplam **24 harika güvenlik, ağ ve denetim aracı** profesyonel bir Sol Menü (Sidebar) üzerinde kategorize edilerek kullanımınıza sunulmuştur.

### 🌟 Özellikler (24 Kapsamlı Modül)
- **Aktif Güvenlik Kalkanları (v3.1 Yenilikleri)**: Bilgisayarınızı siber tehditlerden otomatik korumak üzere tasarlanan Hosts Kalkanı, Zararlı İşlem Avcısı, Kamera/Mikrofon Bekçisi, Ağ İçi Siber Kapan (Honeypot Tuzakları), USB Aşısı ve Windows Genel Güvenlik Zırhı.
- **Ağ ve Yönetim Merkezi**: Ağ Tarayıcı (Yerleşik ARP tespiti), Eşzamanlı Parçacıklı Port Tarayıcı, Arka Planda Canlı Soket ve Bağlantı İzleyici, Otomatik Güvenlik Skoru Gösterge Paneli.
- **Kriptografi Şifreleme**: Gelişmiş Hash Üretici (MD5, SHA ailesi), Base64 Kodlayıcı, Kimsenin bulamayacağı anahtarlı (XOR) Metin Şifreleyici.
- **Sistem Mühendisliği**: Hızlı ICMP Ping, Ağ Mühendisleri için Subnet (Alt Ağ) Makinesi, DNS Analizi, Sahte MAC Yaratıcı/Doğrulayıcı, İşlemci ve RAM Dökümü.
- **Kişisel Araçlar**: Parola Zafiyet Testi, Yüksek Güvenlikli Rastgele Şifre Matrisi.
- **Raporlama Sistemi**: Tüm saldırı ve ağ tespitlerinizi iş arkadaşlarınıza ya da yönetime saniyeler içinde **PDF** veya **Excel (CSV)** olarak dökme imkânı.

### 🚀 Kullanım ve Kurulum (Türkçe)
1. Bilgisayarınızda Python 3.10 veya daha güncel bir sürümün yüklü olduğundan emin olun.
2. Projeyi indirdikten sonra terminalinizde gerekli altyapıyı kurun:
   ```bash
   pip install -r requirements.txt
   ```
3. Uygulamayı başlatın:
   ```bash
   python main.py
   ```
*(Not: Sistemi tehlikelere karşı kalıcı koruyan USB Aşısı ve Hosts Kalkanı gibi araçlar, Windows işletim sisteminizin korumalı çekirdek/kayıt defterinde değişiklik yapacağı için programı "Yönetici Olarak Çalıştır" ile açmanız tavsiye edilir).*

---
🔒 *Disclaimer / Yasal Uyarı:* This tool is meant for educational and administrative purposes on networks you own or have permission to scan. / Bu araç yalnızca kendi ağlarınızda veya analiz izniniz olan ağlarda eğitim/yönetim amacıyla kullanılmak üzere tasarlanmıştır. Yasadışı kullanımlardan geliştirici sorumlu tutulamaz.
