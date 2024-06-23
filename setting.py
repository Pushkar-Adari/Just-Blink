import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Main Window')
        self.setGeometry(100, 100, 400, 300)

        self.settings_button = QPushButton('Settings', self)
        self.settings_button.clicked.connect(self.open_settings)
        self.settings_button.setGeometry(150, 150, 100, 50)

    def open_settings(self):
        settings_dialog = QDialog(self)
        settings_dialog.setWindowTitle('Settings')
        settings_layout = QVBoxLayout()

        label = QLabel('Settings content goes here.')
        settings_layout.addWidget(label)

        settings_dialog.setLayout(settings_layout)
        settings_dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
