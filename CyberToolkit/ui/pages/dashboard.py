from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt

try:
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

def create_info_box(title, text):
    box = QWidget()
    box.setStyleSheet("background-color: #1e293b; border-left: 4px solid #3b82f6; padding: 10px; margin-bottom: 20px;")
    layout = QVBoxLayout(box)
    layout.setContentsMargins(10, 10, 10, 10)
    lbl_title = QLabel(f"ℹ️ {title}")
    lbl_title.setStyleSheet("font-weight: bold; color: #3b82f6; border: none;")
    layout.addWidget(lbl_title)
    lbl_text = QLabel(text)
    lbl_text.setWordWrap(True)
    lbl_text.setStyleSheet("color: #cbd5e1; border: none; font-size: 13px;")
    layout.addWidget(lbl_text)
    return box

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Gösterge Paneli")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        layout.addWidget(create_info_box("Bu özellik nedir?", "Ağınızın ve uygulamanın genel durumunu özetleyen kontrol panelidir."))
        
        cards_layout = QHBoxLayout()
        self.lbl_devices = self._create_card(cards_layout, "Toplam Cihaz", "0")
        self.lbl_ports = self._create_card(cards_layout, "Açık Portlar", "0")
        self.lbl_connections = self._create_card(cards_layout, "Aktif Bağlantılar", "0")
        self.lbl_score = self._create_card(cards_layout, "Güvenlik Skoru", "100", "#10b981")
        layout.addLayout(cards_layout)
        
        if HAS_MATPLOTLIB:
            self.figure = Figure(figsize=(5, 3), facecolor='#1e293b')
            self.canvas = FigureCanvas(self.figure)
            self.ax = self.figure.add_subplot(111)
            self.ax.set_facecolor('#0f172a')
            self.ax.tick_params(colors='white')
            for spine in self.ax.spines.values():
                spine.set_color('#334155')
            self.ax.set_title("Zaman İçinde Taramalar", color='white')
            layout.addWidget(self.canvas)
            self.update_graph([1, 2, 3, 4, 5], [10, 15, 7, 20, 30])
        else:
            layout.addWidget(QLabel("Matplotlib bulunamadı. Grafikler kapalı."))
            
        layout.addStretch()

    def _create_card(self, parent_layout, title, value, color="#3b82f6"):
        frame = QFrame()
        frame.setStyleSheet("QFrame { background-color: #1e293b; border-radius: 10px; border: 1px solid #334155; }")
        flayout = QVBoxLayout(frame)
        t = QLabel(title)
        t.setStyleSheet("color: #94a3b8; font-size: 14px;")
        t.setAlignment(Qt.AlignCenter)
        flayout.addWidget(t)
        v = QLabel(value)
        v.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: bold;")
        v.setAlignment(Qt.AlignCenter)
        flayout.addWidget(v)
        parent_layout.addWidget(frame)
        return v
        
    def update_graph(self, x_data, y_data):
        if not HAS_MATPLOTLIB: return
        self.ax.clear()
        self.ax.set_facecolor('#0f172a')
        self.ax.tick_params(colors='white')
        self.ax.set_title("Zaman İçinde Taramalar", color='white')
        for spine in self.ax.spines.values():
            spine.set_color('#334155')
        self.ax.plot(x_data, y_data, color='#10b981', marker='o', linestyle='-')
        self.canvas.draw()

    def update_stats(self, devices, ports, connections, score):
        self.lbl_devices.setText(str(devices))
        self.lbl_ports.setText(str(ports))
        self.lbl_connections.setText(str(connections))
        self.lbl_score.setText(str(score))
        if score > 80:
            self.lbl_score.setStyleSheet("color: #10b981; font-size: 28px; font-weight: bold;")
        elif score > 50:
            self.lbl_score.setStyleSheet("color: #f59e0b; font-size: 28px; font-weight: bold;")
        else:
            self.lbl_score.setStyleSheet("color: #ef4444; font-size: 28px; font-weight: bold;")
