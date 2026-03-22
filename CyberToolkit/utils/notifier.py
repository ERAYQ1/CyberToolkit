from PySide6.QtWidgets import QSystemTrayIcon, QStyle, QApplication

class Notifier:
    """
    Handles system notifications (pop-ups/toast) utilizing PySide6's QSystemTrayIcon.
    Requires the application to create the system tray icon first.
    """
    
    def __init__(self, app: QApplication, parent=None):
        self.tray_icon = QSystemTrayIcon(parent)
        
        # Use a standard info icon for the tray
        icon = app.style().standardIcon(QStyle.SP_ComputerIcon)
        self.tray_icon.setIcon(icon)
        self.tray_icon.show()

    def notify(self, title: str, message: str, msg_type: str = "info"):
        """
        Shows a toast notification to the OS desktop.
        msg_type can be 'info', 'warning', or 'critical'.
        """
        icon_type = QSystemTrayIcon.Information
        if msg_type == "warning":
            icon_type = QSystemTrayIcon.Warning
        elif msg_type == "critical":
            icon_type = QSystemTrayIcon.Critical

        # duration in milliseconds
        self.tray_icon.showMessage(title, message, icon_type, 3000)
