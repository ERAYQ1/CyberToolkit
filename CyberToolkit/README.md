# CyberToolkit v2.0

CyberToolkit, tamamen internet bağımsız, harici bir kütüphane/sürücü gerektirmeyen (WinPcap vb.), yerel sisteminiz üzerinde yüksek performansla çalışan açık kaynaklı bir siber güvenlik yardımcı araç setidir. PySide6 ile geliştirilmiştir.

## İçerisinde Bulunan Araçlar

- **Ağ/Tarama Servisleri**: Tek Tıkla Ağ Tarayıcı, Çok Parçacıklı Port Tarayıcı, Aktif/Canlı Bağlantı İzleyici.
- **Kriptografi / Şifreleme**: Hash Oluşturucu, Base64 Dönüştürücü, XOR Metin Şifreleyici.
- **Network / Sistem**: ICMP Ping Aracı, Subnet (Alt Ağ) Hesaplayıcı, DNS Sorgusu, MAC Üretici.
- **Yardımcılar**: Şifre Güç Analizcisi (Kırılma Süresi), Güvenli Parola Oluşturucu, URL Formatlayıcı.
- **Raporlama**: Tüm geçmiş yapılan işlemleri görüntüleme ve tek tuşla **PDF / CSV** dökümü alma işlemi.

## Kurulum ve Çalıştırma

1. Python 3.10+ kurulu olduğundan emin olun.
2. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
3. Uygulamayı başlatın:
   ```bash
   python main.py
   ```

*(Eğer Scapy gibi farklı hatalar aldıysanız, bu v2.0 sürümü ile birlikte tüm 3. parti ağ analiz kütüphaneleri yerini standart Socket/Subprocess Python kütüphanelerine bırakmıştır, temiz şekilde çalışacaktır.)*
