import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                               QPushButton, QMessageBox)
from PySide6.QtGui import QFont

from modules.report_generator import ReportGenerator

class ReportsPage(QWidget):
    def __init__(self, user_system):
        super().__init__()
        self.user_system = user_system
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        header = QLabel("Generate Reports")
        header.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.setStyleSheet("color: #00e676;")
        layout.addWidget(header)
        
        layout.addWidget(QLabel("Export your scan history into actionable reports."))
        
        btn_pdf = QPushButton("📥 Export to PDF")
        btn_pdf.setMinimumHeight(50)
        btn_pdf.clicked.connect(self.export_pdf)
        
        btn_csv = QPushButton("📥 Export to CSV")
        btn_csv.setMinimumHeight(50)
        btn_csv.clicked.connect(self.export_csv)
        
        layout.addWidget(btn_pdf)
        layout.addWidget(btn_csv)
        
        layout.addStretch()

    def export_pdf(self):
        user_data = self.user_system.get_user_data()
        history = user_data.get("scan_history", [])
        
        if not history:
            QMessageBox.warning(self, "No Data", "Scan history is empty. Nothing to export.")
            return

        total_scans = len(history)
        port_scans = sum(1 for x in history if x['type'] == 'Port Scan')
        net_scans = sum(1 for x in history if x['type'] == 'Network Scan')

        summary = {
            "Total Scans Performed": str(total_scans),
            "Port Scans": str(port_scans),
            "Network Scans": str(net_scans)
        }
        
        # Build list of finding strings
        items = []
        for h in history[-10:]: # Include up to last 10 scans
            if h['type'] == 'Port Scan':
                target = h['data'].get('target', 'Unknown')
                count = len(h['data'].get('open_ports', []))
                items.append(f"Port Scan on {target}: Found {count} open ports.")
            elif h['type'] == 'Network Scan':
                target = h['data'].get('range', 'Unknown')
                count = len(h['data'].get('devices', []))
                items.append(f"Network Scan on {target}: Found {count} devices.")
        
        output_file = f"data/report_{self.user_system.current_user}.pdf"
        success, msg = ReportGenerator.generate_pdf_report(
            output_file, "CyberToolkit User Scan Report", summary, items
        )
        
        if success:
            QMessageBox.information(self, "Success", f"PDF Exported successfully to:\n{os.path.abspath(output_file)}")
        else:
            QMessageBox.critical(self, "Error", f"Failed to generate PDF:\n{msg}")

    def export_csv(self):
        # Dump a summarized table
        user_data = self.user_system.get_user_data()
        history = user_data.get("scan_history", [])
        
        if not history:
            QMessageBox.warning(self, "No Data", "Scan history is empty. Nothing to export.")
            return
            
        headers = ["Timestamp", "Scan Type", "Target/Range", "Count"]
        rows = []
        for h in history:
            ts = h.get('timestamp')
            t = h.get('type')
            if t == 'Port Scan':
                target = h['data'].get('target', 'Unknown')
                count = len(h['data'].get('open_ports', []))
            elif t == 'Network Scan':
                target = h['data'].get('range', 'Unknown')
                count = len(h['data'].get('devices', []))
            else:
                target = "N/A"
                count = 0
            rows.append([ts, t, target, count])
            
        output_file = f"data/report_{self.user_system.current_user}.csv"
        success, msg = ReportGenerator.export_to_csv(output_file, headers, rows)
        
        if success:
            QMessageBox.information(self, "Success", f"CSV Exported successfully to:\n{os.path.abspath(output_file)}")
        else:
            QMessageBox.critical(self, "Error", msg)
