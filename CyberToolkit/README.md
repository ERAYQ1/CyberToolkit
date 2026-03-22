# 🛡️ CyberToolkit v2.0

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-GUI-green.svg)
![License](https://img.shields.io/badge/License-MIT-purple.svg)

*(🇹🇷 Türkçe açıklamalar aşağıdadır / Turkish description is below)*

**CyberToolkit** is an advanced, open-source, and entirely offline desktop cybersecurity utility suite. Built meticulously with PySide6, it requires no external packet-sniffing drivers (such as WinPcap or Npcap) and runs seamlessly using Python's native socket and subprocess capabilities. 

From network reconnaissance to cryptography utilities, CyberToolkit provides all the essential tools a cybersecurity enthusiast or network administrator needs in one modern, AI-free desktop application.

### 🌟 English Features
- **Network & Scanning**: One-Click Network Discovery (Native ARP), Multi-threaded Port Scanner, Live Suspicious Connection Monitor.
- **Cryptography & Encoding**: Hash Generator (MD5, SHA1, SHA256), Base64 Encoder/Decoder, XOR Text Encryptor.
- **System Utilities**: High-performance ICMP Ping Tool, IPv4 Subnet Calculator, DNS & Reverse DNS Lookup, MAC Address Generator/Validator, Detailed System Hardware Info.
- **Security Tools**: Password Strength Analyzer (with Crack Time Estimation), Secure Customizable Password Generator, URL Formatter.
- **Reporting System**: Export all historical tasks and scanning logs to **PDF** or **CSV** formats instantly for professional audits.

### 🚀 Installation (English)
1. Ensure Python 3.10+ is installed on your system.
2. Clone this repository and install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

---

## 🇹🇷 Türkçe Açıklamalar

**CyberToolkit**, tamamen internetten bağımsız çalışan, harici bir sürücü (WinPcap vb.) indirme zorunluluğunu rafa kaldıran ve bilgisayarınızda yüksek performansla çalışan yerel bir siber güvenlik masaüstü uygulamasıdır. İçerisindeki 10+ yerel araç ile ağ güvenliğinizi ve kriptografik ihtiyaçlarınızı tek bir modern programdan yönetmenizi sağlar.

### 🌟 Gelişmiş Özellikler
- **Ağ ve Tarama Servisleri**: Tek Tıkla Cihaz Tespit Eden Ağ Tarayıcı (Subprocess/ARP), Çok Parçacıklı Hızlı Port Tarayıcı, Arka planda anlık haberleşmeleri dinleyen Canlı Bağlantı İzleyici.
- **Kriptografi ve Şifreleme**: Gelişmiş Hash Oluşturucu (MD5, SHA Ailesi), Base64 Dönüştürücü, İki yönlü Metin Şifreleyici (Key tabanlı XOR).
- **Ağ / Sistem Araçları**: Eşzamanlı ICMP Ping Aracı, Profesyoneller için CIDR Alt Ağ (Subnet) Hesaplayıcı, DNS ve Ters DNS Sorgusu, Donanım MAC Adresi Üretici, Gerçek Zamanlı RAM ve İşlemci Dökümü.
- **Güvenlik Yardımcıları**: Akıllı Şifre Kırılma Süresi Analizcisi, Yüksek Güvenlikli Parola Üretici, URL Güvenlik Kodlayıcısı.
- **Raporlama Sistemi**: Gerçekleştirdiğiniz tüm güvenlik taramalarını saniyeler içinde yönetime sunmak üzere **PDF** veya **CSV (Excel)** olarak masaüstüne çıkartabilme imkânı.

### 🚀 Kullanım ve Kurulum (Türkçe)
1. Bilgisayarınızda Python 3.10 veya daha güncel bir sürümün yüklü olduğundan emin olun.
2. Projeyi bilgisayarınıza indirdikten sonra terminalinizde şu komutla kütüphaneleri kurun:
   ```bash
   pip install -r requirements.txt
   ```
3. Uygulamayı başlatın:
   ```bash
   python main.py
   ```

*(Not: CyberToolkit v2.0 ile birlikte tüm yorucu 3. parti ağ analiz kütüphaneleri projeden çıkartılarak, tamamen standart Python kütüphaneleri ile baştan kodlanmıştır. İlave bir ayar yapmadan anında çalışır.)*

---
🔒 *Disclaimer / Yasal Uyarı:* This tool is meant for educational and administrative purposes on networks you own or have permission to scan. / Bu araç yalnızca kendi ağlarınızda veya analiz izniniz olan ağlarda eğitim/yönetim amacıyla kullanılmak üzere tasarlanmıştır. Yasadışı kullanımlardan geliştirici sorumlu tutulamaz.
