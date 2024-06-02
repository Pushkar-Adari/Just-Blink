import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from app_ui import Ui_Home

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Home()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
