import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def export_pdf_report(history_data, file_path):
    """
    Exports the scan history data into a simple PDF report.
    """
    try:
        c = canvas.Canvas(file_path, pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, "CyberToolkit Security Report")
        
        c.setFont("Helvetica", 10)
        c.drawString(50, 730, f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        y = 700
        c.setFont("Helvetica", 12)
        for entry in history_data:
            c.drawString(50, y, f"Scan Type: {entry.get('type')}")
            y -= 15
            details = entry.get('details', {})
            for k, v in details.items():
                c.drawString(70, y, f"{k}: {v}")
                y -= 15
            y -= 10
            
            if y < 50:
                c.showPage()
                c.setFont("Helvetica", 12)
                y = 750
                
        c.save()
        return True
    except Exception as e:
        print(f"Failed to generate PDF: {e}")
        return False
