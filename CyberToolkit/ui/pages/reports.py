import os
import csv
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QHBoxLayout
from PySide6.QtCore import Qt
from utils.database import db
from utils.pdf_report import export_pdf_report
from .dashboard import create_info_box

class ReportsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Raporlar")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        layout.addWidget(create_info_box("Bu özellik nedir?", "Tüm tarama ve analiz geçmişinizi dışa aktarmanızı sağlar. Seçtiğiniz formata göre (PDF veya CSV) masaüstünüze profesyonel bir rapor kaydeder."))
        
        btn_layout = QHBoxLayout()
        
        self.btn_pdf = QPushButton("PDF Olarak Dışa Aktar")
        self.btn_pdf.clicked.connect(self.export_pdf)
        btn_layout.addWidget(self.btn_pdf)
        
        self.btn_csv = QPushButton("CSV (Excel) Olarak Dışa Aktar")
        self.btn_csv.clicked.connect(self.export_csv)
        btn_layout.addWidget(self.btn_csv)
        
        layout.addLayout(btn_layout)
        layout.addStretch()

    def export_pdf(self):
        hist = db.get_history()
        if not hist:
            QMessageBox.warning(self, "Hata", "Dışa aktarılacak geçmiş bulunamadı.")
            return
            
        home = os.path.expanduser("~")
        path = os.path.join(home, "Desktop", "CyberToolkit_Raporu.pdf")
        
        if export_pdf_report(hist, path):
            QMessageBox.information(self, "Başarılı", f"PDF raporu şuraya kaydedildi:\n{path}")
        else:
            QMessageBox.critical(self, "Hata", "PDF oluşturulamadı.")

    def export_csv(self):
        hist = db.get_history()
        if not hist:
            QMessageBox.warning(self, "Hata", "Dışa aktarılacak geçmiş bulunamadı.")
            return
            
        home = os.path.expanduser("~")
        path = os.path.join(home, "Desktop", "CyberToolkit_Raporu.csv")
        
        try:
            with open(path, "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["İşlem Türü", "Detaylar"])
                for h in hist:
                    writer.writerow([h.get("type", "Bilinmiyor"), str(h.get("details", ""))])
            QMessageBox.information(self, "Başarılı", f"CSV raporu şuraya kaydedildi:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"CSV oluşturulamadı: {e}")
