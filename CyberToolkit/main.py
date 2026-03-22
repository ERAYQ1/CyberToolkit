import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow, LoginWindow

# Force the working directory logic if needed, but not necessary here

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Check if there are any users in DB. If yes, show login. If no, show register/login.
    
    def on_login_success(username):
        global window
        window = MainWindow(username)
        window.show()

    login = LoginWindow(app.setStyleSheet, on_login_success)
    login.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
