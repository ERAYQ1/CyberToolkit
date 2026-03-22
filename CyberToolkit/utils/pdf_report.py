import datetime

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False


def export_pdf_report(history_data, file_path):
    """Exports scan history data into a PDF report."""
    if not HAS_REPORTLAB:
        return False

    try:
        c = canvas.Canvas(file_path, pagesize=letter)
        _, height = letter

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "CyberToolkit Security Report")

        c.setFont("Helvetica", 10)
        c.drawString(50, height - 70, f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        y = height - 100
        c.setFont("Helvetica", 12)

        for entry in history_data:
            c.drawString(50, y, f"Scan Type: {entry.get('type', 'Unknown')}")
            y -= 15
            for k, v in entry.get("details", {}).items():
                c.drawString(70, y, f"{k}: {v}")
                y -= 15
            y -= 10

            if y < 50:
                c.showPage()
                c.setFont("Helvetica", 12)
                y = height - 50

        c.save()
        return True
    except Exception:
        return False
