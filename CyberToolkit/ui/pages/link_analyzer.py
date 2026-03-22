from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit
from PySide6.QtCore import Qt
from modules.link_analyzer import LinkAnalyzer

class LinkAnalyzerPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        self.analyzer = LinkAnalyzer()
        self.analyzer.result_found.connect(self.on_result)
        
        title = QLabel("Zararlı Link (Oltalama) Çözümleyici")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #ef4444;")
        self.layout.addWidget(title)
        
        desc = QLabel("Size gelen şüpheli e-posta, SMS veya mesajlardaki garip linkleri tarayıcıda açmadan buraya yapıştırın. Sistem arkaplanda siteyi kontrol edip şifrenizi çalmaya çalışan 'Typosquatting' veya maskelenmiş yönlendirmeleri tespit eder.")
        desc.setWordWrap(True)
        self.layout.addWidget(desc)
        
        row = QHBoxLayout()
        self.inp_url = QLineEdit()
        self.inp_url.setPlaceholderText("Analiz edilecek URL'yi yapıştırın (Örn: http://g00gle-secure-login.com)")
        self.inp_url.returnPressed.connect(self.run_analysis)
        
        self.btn_scan = QPushButton("🔬 Siteyi Parçala ve Analiz Et")
        self.btn_scan.setStyleSheet("background-color: #ef4444; color: white;")
        self.btn_scan.clicked.connect(self.run_analysis)
        
        row.addWidget(self.inp_url)
        row.addWidget(self.btn_scan)
        self.layout.addLayout(row)
        
        self.txt_result = QTextEdit()
        self.txt_result.setReadOnly(True)
        self.txt_result.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.txt_result)

    def run_analysis(self):
        url = self.inp_url.text().strip()
        if not url: return
        self.btn_scan.setEnabled(False)
        self.txt_result.setText(f"Hedef analiz ediliyor: {url}\nLütfen bekleyin...")
        self.analyzer.analyze(url)

    def on_result(self, report):
        self.btn_scan.setEnabled(True)
        self.txt_result.clear()
        
        self.txt_result.append(f"<b>Hedef Web Adresi:</b> {report['url']}")
        self.txt_result.append(f"<b>Gerçek Yönlendirme Bitiş Noktası:</b> {report['redirects_to']}")
        self.txt_result.append(f"<b>Sunucu Kimliği:</b> {report['server']}\n")
        
        if report['is_phishing']:
            self.txt_result.append("<h2 style='color:#ef4444;'>[KRİTİK UYARI] BU SİTE OLTALAMA AMACIYLA KURGULANMIŞTIR! KESİNLİKLE ŞİFRE GİRMEYİN.</h2>")
            
        if report['warnings']:
            self.txt_result.append("<b>Tespit Edilen Güvenlik Alarmları:</b>")
            for w in report['warnings']:
                self.txt_result.append(f" ⚠️ {w}")
        else:
            self.txt_result.append("<b style='color:#10b981;'>Sistem herhangi bir oltalama, sahte yönlendirme veya güvenilmez uzantı tespit etmedi. Yinede dikkatli olun.</b>")
