from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                               QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox)
from PySide6.QtCore import Qt
from modules.password_manager import PasswordVault

class PasswordManagerPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        title = QLabel("🔐 Şifre Kasası")
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #8b5cf6;")
        layout.addWidget(title)

        desc = QLabel("Tüm şifrelerinizi tek bir ana parola ile şifreleyerek güvenle saklayın. Veriler AES-256 ile şifrelenir ve sadece siz açabilirsiniz.")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #94a3b8; font-size: 13px;")
        layout.addWidget(desc)

        # Master password row
        master_row = QHBoxLayout()
        self.inp_master = QLineEdit()
        self.inp_master.setPlaceholderText("Ana Parola (Kasayı açmak için)")
        self.inp_master.setEchoMode(QLineEdit.Password)
        self.inp_master.setStyleSheet("padding: 10px; font-size: 14px; border-radius: 6px; border: 1px solid #334155; background-color: #1e293b; color: white;")
        master_row.addWidget(self.inp_master)

        self.btn_unlock = QPushButton("🔓 Kasayı Aç")
        self.btn_unlock.setStyleSheet("background-color: #8b5cf6; color: white; padding: 10px 20px; font-weight: bold; border-radius: 6px;")
        self.btn_unlock.clicked.connect(self.unlock_vault)
        master_row.addWidget(self.btn_unlock)
        layout.addLayout(master_row)

        # Add entry row
        add_row = QHBoxLayout()
        self.inp_site = QLineEdit()
        self.inp_site.setPlaceholderText("Site / Uygulama Adı")
        self.inp_site.setStyleSheet("padding: 8px; border-radius: 6px; border: 1px solid #334155; background-color: #1e293b; color: white;")
        add_row.addWidget(self.inp_site)

        self.inp_user = QLineEdit()
        self.inp_user.setPlaceholderText("Kullanıcı Adı")
        self.inp_user.setStyleSheet("padding: 8px; border-radius: 6px; border: 1px solid #334155; background-color: #1e293b; color: white;")
        add_row.addWidget(self.inp_user)

        self.inp_pass = QLineEdit()
        self.inp_pass.setPlaceholderText("Şifre")
        self.inp_pass.setStyleSheet("padding: 8px; border-radius: 6px; border: 1px solid #334155; background-color: #1e293b; color: white;")
        add_row.addWidget(self.inp_pass)

        self.btn_add = QPushButton("➕ Ekle")
        self.btn_add.setStyleSheet("background-color: #10b981; color: white; padding: 8px 16px; font-weight: bold; border-radius: 6px;")
        self.btn_add.clicked.connect(self.add_entry)
        add_row.addWidget(self.btn_add)
        layout.addLayout(add_row)

        # Table
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Site / Uygulama", "Kullanıcı Adı", "Şifre"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("""
            QTableWidget { background-color: #0f172a; color: #e2e8f0; gridline-color: #334155; border: 1px solid #1e293b; border-radius: 8px; font-size: 13px; alternate-background-color: #1e293b; }
            QHeaderView::section { background-color: #1e293b; color: #94a3b8; border: none; padding: 8px; font-size: 13px; font-weight: bold; }
        """)
        layout.addWidget(self.table)

        self.btn_del = QPushButton("🗑️ Seçili Kaydı Sil")
        self.btn_del.setStyleSheet("background-color: #ef4444; color: white; padding: 8px; font-weight: bold; border-radius: 6px;")
        self.btn_del.clicked.connect(self.delete_entry)
        layout.addWidget(self.btn_del)

        self.vault = PasswordVault()
        self._unlocked = False

    def unlock_vault(self):
        pwd = self.inp_master.text().strip()
        if not pwd:
            QMessageBox.warning(self, "Hata", "Lütfen ana parolanızı girin.")
            return

        self.vault.unlock(pwd)
        entries = self.vault.get_entries()

        if entries is None:
            QMessageBox.warning(self, "Hata", "Yanlış parola veya kasa bozuk.")
            self._unlocked = False
            return

        self._unlocked = True
        self._load_table(entries)
        QMessageBox.information(self, "Başarılı", f"Kasa açıldı. {len(entries)} kayıt bulundu.")

    def _load_table(self, entries):
        self.table.setRowCount(0)
        for e in entries:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(e.get("site", "")))
            self.table.setItem(row, 1, QTableWidgetItem(e.get("user", "")))
            self.table.setItem(row, 2, QTableWidgetItem(e.get("pass", "")))

    def add_entry(self):
        if not self._unlocked:
            QMessageBox.warning(self, "Hata", "Önce kasayı açın.")
            return
        site = self.inp_site.text().strip()
        user = self.inp_user.text().strip()
        pwd = self.inp_pass.text().strip()
        if not site or not pwd:
            return

        self.vault.add_entry(site, user, pwd)
        self.inp_site.clear()
        self.inp_user.clear()
        self.inp_pass.clear()
        self._load_table(self.vault.get_entries())

    def delete_entry(self):
        if not self._unlocked:
            return
        row = self.table.currentRow()
        if row < 0:
            return
        ans = QMessageBox.question(self, "Onay", "Bu kayıt silinsin mi?")
        if ans == QMessageBox.Yes:
            self.vault.delete_entry(row)
            self._load_table(self.vault.get_entries())
