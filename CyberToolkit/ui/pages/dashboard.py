from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt
from utils.translations import t

try:
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


def create_info_box(title, text):
    box = QFrame()
    box.setStyleSheet("""
        QFrame {
            background-color: #1e293b; border-left: 4px solid #3b82f6;
            border-radius: 8px; padding: 12px;
        }
    """)
    layout = QVBoxLayout(box)
    layout.setContentsMargins(12, 8, 12, 8)
    lbl_title = QLabel(f"ℹ️ {title}")
    lbl_title.setStyleSheet("font-weight: bold; color: #3b82f6; border: none; font-size: 13px;")
    layout.addWidget(lbl_title)
    lbl_text = QLabel(text)
    lbl_text.setWordWrap(True)
    lbl_text.setStyleSheet("color: #cbd5e1; border: none; font-size: 12px;")
    layout.addWidget(lbl_text)
    return box


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(18)

        # Header
        header = QHBoxLayout()
        self.title = QLabel(t("dash_title"))
        self.title.setStyleSheet("font-size: 26px; font-weight: bold; color: #10b981;")
        header.addWidget(self.title)
        header.addStretch()

        self.lbl_time = QLabel("")
        self.lbl_time.setStyleSheet("color: #64748b; font-size: 12px;")
        header.addWidget(self.lbl_time)
        layout.addLayout(header)

        self.desc = QLabel(t("dash_desc"))
        self.desc.setWordWrap(True)
        self.desc.setStyleSheet("color: #94a3b8; font-size: 13px;")
        layout.addWidget(self.desc)

        # Stat Cards Row
        cards_row = QHBoxLayout()
        cards_row.setSpacing(14)

        self.lbl_devices = self._make_card(cards_row, t("dash_devices"), "0", "#3b82f6")
        self.lbl_ports = self._make_card(cards_row, t("dash_ports"), "0", "#f59e0b")
        self.lbl_connections = self._make_card(cards_row, t("dash_conns"), "0", "#8b5cf6")
        self.lbl_score = self._make_card(cards_row, t("dash_score"), "100", "#10b981")
        layout.addLayout(cards_row)

        # Graph
        if HAS_MATPLOTLIB:
            self.figure = Figure(figsize=(5, 2.5), facecolor='#1e293b')
            self.canvas = FigureCanvas(self.figure)
            self.canvas.setStyleSheet("border: 1px solid #334155; border-radius: 8px;")
            self.ax = self.figure.add_subplot(111)
            self._style_axes()
            layout.addWidget(self.canvas)
            self.update_graph([1, 2, 3, 4, 5], [10, 15, 7, 20, 30])
        else:
            no_graph = QLabel("ℹ️ Grafik gösterimi için: pip install matplotlib")
            no_graph.setStyleSheet("color: #64748b; font-size: 12px; padding: 20px;")
            no_graph.setAlignment(Qt.AlignCenter)
            layout.addWidget(no_graph)

        layout.addStretch()

    def _make_card(self, parent_layout, title, value, color):
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #1e293b; border-radius: 12px;
                border-left: 5px solid {color}; border: 1px solid #334155;
                border-left: 5px solid {color};
            }}
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 14, 16, 14)
        card_layout.setSpacing(6)

        lbl = QLabel(title)
        lbl.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold; border: none;")
        card_layout.addWidget(lbl)

        val = QLabel(value)
        val.setObjectName("value")
        val.setStyleSheet(f"color: {color}; font-size: 30px; font-weight: bold; border: none;")
        val.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(val)

        parent_layout.addWidget(card)
        return val

    def _style_axes(self):
        self.ax.set_facecolor('#0f172a')
        self.ax.tick_params(colors='#94a3b8', labelsize=8)
        for spine in self.ax.spines.values():
            spine.set_color('#334155')
        self.ax.set_title("Son Tarama Sonuçları", color='#e2e8f0', fontsize=11, pad=10)

    def update_graph(self, x_data, y_data):
        if not HAS_MATPLOTLIB:
            return
        self.ax.clear()
        self._style_axes()
        self.ax.fill_between(x_data, y_data, alpha=0.3, color='#10b981')
        self.ax.plot(x_data, y_data, color='#10b981', marker='o', linewidth=2, markersize=5)
        self.canvas.draw()

    def update_stats(self, devices, ports, connections, score):
        self.lbl_devices.setText(str(devices))
        self.lbl_ports.setText(str(ports))
        self.lbl_connections.setText(str(connections))
        self.lbl_score.setText(str(score))

        if score > 80:
            color = "#10b981"
        elif score > 50:
            color = "#f59e0b"
        else:
            color = "#ef4444"
        self.lbl_score.setStyleSheet(f"color: {color}; font-size: 30px; font-weight: bold; border: none;")
