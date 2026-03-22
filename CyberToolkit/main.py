import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow, LoginWindow


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    def on_login_success(username):
        global window
        window = MainWindow(username)
        window.show()

    login = LoginWindow(app.setStyleSheet, on_login_success)
    login.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
