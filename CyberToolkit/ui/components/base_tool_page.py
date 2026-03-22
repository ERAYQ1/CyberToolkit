from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class BaseToolPage(QWidget):
    def __init__(self, title, description):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #10b981;")
        self.layout.addWidget(lbl_title)
        
        if description:
            lbl_desc = QLabel(description)
            lbl_desc.setWordWrap(True)
            self.layout.addWidget(lbl_desc)
