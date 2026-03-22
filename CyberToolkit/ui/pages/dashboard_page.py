from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class DashboardPage(QWidget):
    """
    Dashboard visualizes key metrics and charts.
    """
    def __init__(self, user_system):
        super().__init__()
        self.user_system = user_system
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        
        header = QLabel("Dashboard Summary")
        header.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.setStyleSheet("color: #00e676;")
        main_layout.addWidget(header)

        # Top Cards Layout (Stats)
        stats_layout = QHBoxLayout()
        
        self.lbl_devices = self.create_stat_card("Devices Found\n(Latest)", "0")
        self.lbl_ports = self.create_stat_card("Open Ports\n(Latest)", "0")
        self.lbl_conns = self.create_stat_card("Active Conns", "0")
        self.lbl_score = self.create_stat_card("Security Score", "100")
        
        stats_layout.addWidget(self.lbl_devices)
        stats_layout.addWidget(self.lbl_ports)
        stats_layout.addWidget(self.lbl_conns)
        stats_layout.addWidget(self.lbl_score)
        
        main_layout.addLayout(stats_layout)

        # Charts Area
        chart_layout = QHBoxLayout()
        
        # Risk Distribution Chart (Pie)
        self.fig_pie = Figure(figsize=(4, 3), dpi=100)
        self.fig_pie.patch.set_facecolor('#1a1c29')
        self.canvas_pie = FigureCanvas(self.fig_pie)
        self.ax_pie = self.fig_pie.add_subplot(111)
        
        self.update_pie_chart([2, 5, 10], ["High", "Medium", "Low"])
        
        chart_layout.addWidget(self.canvas_pie)

        main_layout.addLayout(chart_layout)
        main_layout.addStretch()

    def create_stat_card(self, title, val):
        frame = QFrame()
        frame.setObjectName("card")
        frame.setMinimumSize(150, 100)
        
        layout = QVBoxLayout(frame)
        
        lbl_val = QLabel(val)
        lbl_val.setFont(QFont("Segoe UI", 24, QFont.Bold))
        lbl_val.setAlignment(Qt.AlignCenter)
        lbl_val.setStyleSheet("color: #ffffff;")
        
        # Dynamically attach title as property if needed or just use layout child
        lbl_title = QLabel(title)
        lbl_title.setAlignment(Qt.AlignCenter)
        lbl_title.setStyleSheet("color: #888888;")
        
        layout.addWidget(lbl_val)
        layout.addWidget(lbl_title)
        
        # Keep a reference to the label so we can update it
        frame.value_label = lbl_val
        return frame

    def update_pie_chart(self, sizes, labels):
        self.ax_pie.clear()
        colors = ['#ff5555', '#ffb86c', '#00e676'] # Red, Orange, Green
        
        # Text color adjusting for dark mode
        textprops = {"color": "white"}
        
        # Handle all zeros
        if sum(sizes) == 0:
            sizes = [1]
            labels = ["No Data"]
            colors = ['#282a36']
            
        self.ax_pie.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', textprops=textprops, startangle=90)
        self.ax_pie.axis('equal')
        self.canvas_pie.draw_idle()

    def update_stats(self, devices=None, ports=None, conns=None, score=None):
        if devices is not None:
            self.lbl_devices.value_label.setText(str(devices))
        if ports is not None:
            self.lbl_ports.value_label.setText(str(ports))
        if conns is not None:
            self.lbl_conns.value_label.setText(str(conns))
        if score is not None:
            self.lbl_score.value_label.setText(str(score))
            color = "#00e676" if score >= 80 else ("#ffb86c" if score >= 50 else "#ff5555")
            self.lbl_score.value_label.setStyleSheet(f"color: {color};")
