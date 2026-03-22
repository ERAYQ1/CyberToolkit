# 🛡️ CyberToolkit

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-GUI-green.svg)
![License](https://img.shields.io/badge/License-MIT-purple.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

> **⚠️ YASAL UYARI / LEGAL DISCLAIMER**  
> Bu araç sadece kendi cihazlarınızın güvenliğini denetlemek ve eğitim amacıyla geliştirilmiştir. Yasadışı kullanımlardan geliştirici sorumlu tutulamaz.  
> This tool is for personal security auditing and educational use only. The developer assumes no liability for misuse.

---

## 📖 Proje Hakkında / About

CyberToolkit, Windows kullanıcıları için tamamen yerel çalışan, modern arayüzlü bir kişisel bilgisayar güvenlik ve ağ analiz uygulamasıdır. İnternete bağlı olmadan tüm taramalar ve analizler cihazınızın içinde çalışır.

## 🌍 Çoklu Dil Desteği / Multi-Language

Uygulama **3 dilde** kullanılabilir:
- 🇹🇷 Türkçe (varsayılan)
- 🇬🇧 English
- 🇩🇪 Deutsch

Dil değişikliği **⚙️ Ayarlar** sayfasından yapılabilir.

---

## 🌟 Özellikler / Features (16 Araç)

### 🕵️ Ağ ve Sistem Tarama
| Araç | Açıklama |
|------|----------|
| 📊 Gösterge Paneli | Güvenlik skoru, canlı istatistikler, grafik |
| ⚡ Ağ Hız Testi | Ping, jitter ve bant genişliği ölçümü |
| 📡 Ağa Bağlı Cihazları Bul | Ağınızdaki tüm cihazları (telefon, TV, yazıcı) tespit eder |
| 🔍 Açık Port Tarayıcı | IP üzerindeki açık portları ve servisleri tespit eder |

### 🛡️ Bilgisayar Koruması
| Araç | Açıklama |
|------|----------|
| 🦠 Virüs / Zararlı Avcısı | Arka plandaki şüpheli işlemleri tarar |
| 🛡️ Reklam / Telemetri Kalkanı | Zararlı siteleri hosts dosyası üzerinden engeller |
| 💉 USB Bellek Aşısı | AutoRun virüs bulaşmasını önler |
| 🔒 Windows Güvenlik Zırhı | UAC ve Defender durumunu kontrol eder |
| 🔗 Şüpheli Link Analizi | Oltalama linklerini güvenle analiz eder |

### 🔧 Kullanıcı Araçları
| Araç | Açıklama |
|------|----------|
| 📶 Wi-Fi Şifreleri | Kayıtlı Wi-Fi ağlarının şifrelerini gösterir |
| 🚀 Başlangıç Programları | Otomatik başlayan programları yönetir |
| 🧹 Disk Temizleyici | Geçici dosya ve önbellekleri temizler |
| 🔐 Şifre Kasası | AES-256 şifreli kişisel şifre yöneticisi |

### 📊 Diğer
| Araç | Açıklama |
|------|----------|
| 📜 Tarama Geçmişi | Tüm analiz kayıtlarını gösterir |
| 📄 Rapor Çıktısı | PDF ve CSV dışa aktarma |
| ⚙️ Ayarlar | Tema ve dil değiştirme |

---

## 🚀 Kurulum / Installation

### Gereksinimler
- Python 3.10+
- Windows 10/11

### Başlatma
```bash
git clone <repo-url>
cd CyberToolkit
pip install -r requirements.txt
python main.py
```

> **Not:** Bazı özellikler (USB Aşısı, Hosts Kalkanı, Windows Zırhı) yönetici yetkisi gerektirir. Programı **sağ tık → Yönetici olarak çalıştır** ile başlatmanız önerilir.

---

## 📦 Teknolojiler / Technologies

| Teknoloji | Kullanım |
|-----------|----------|
| Python 3.10+ | Ana dil |
| PySide6 (Qt6) | GUI Framework |
| psutil | Sistem izleme |
| matplotlib | Grafik çizimi |
| reportlab | PDF rapor üretimi |
| cryptography | Şifre kasası (AES-256/Fernet) |

---

## 📁 Proje Yapısı / Project Structure

```
CyberToolkit/
├── main.py                  # Uygulama giriş noktası
├── requirements.txt         # Python bağımlılıkları
├── README.md
├── .gitignore
├── modules/                 # İş mantığı (backend)
│   ├── background_scan.py
│   ├── disk_cleaner.py
│   ├── hosts_blocker.py
│   ├── link_analyzer.py
│   ├── malware_scanner.py
│   ├── network_scanner.py
│   ├── password_manager.py
│   ├── port_scanner.py
│   ├── speed_test.py
│   ├── startup_manager.py
│   ├── usb_vaccine.py
│   ├── wifi_passwords.py
│   └── win_hardening.py
├── ui/                      # Arayüz (frontend)
│   ├── main_window.py
│   ├── sidebar.py
│   ├── themes.py
│   ├── components/
│   │   └── base_tool_page.py
│   └── pages/               # Her araç için UI sayfası
│       ├── dashboard.py
│       ├── network_scanner.py
│       ├── port_scanner.py
│       ├── ... (16 sayfa)
│       └── settings.py
└── utils/                   # Yardımcı modüller
    ├── database.py
    ├── logger.py
    ├── notifier.py
    ├── pdf_report.py
    └── translations.py
```

---

## 🤝 Katkıda Bulunma / Contributing

1. Bu repoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'feat: yeni özellik eklendi'`)
4. Branch'i push edin (`git push origin feature/yeni-ozellik`)
5. Pull Request açın

---

## 📄 Lisans / License

Bu proje MIT Lisansı ile lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.
