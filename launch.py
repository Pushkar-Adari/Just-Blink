import sys
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow
from app_ui import Ui_Home
class Ui_HomeWrapper(QObject):
    mousePressed = pyqtSignal(QPoint)
    mouseMoved = pyqtSignal(QPoint)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Home()

    def setupUi(self, Home):
        self.ui.setupUi(Home)

        self.ui.TitleBar.mousePressEvent = self.mousePressEvent
        self.ui.TitleBar.mouseMoveEvent = self.mouseMoveEvent

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mousePressed.emit(event.globalPos())

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.mouseMoved.emit(event.globalPos())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(800, 600)
        self.dragPos = QPoint()

        self.ui_wrapper = Ui_HomeWrapper(self)
        self.ui_wrapper.setupUi(self)

        # Expose the signals from Ui_HomeWrapper
        self.mousePressed = self.ui_wrapper.mousePressed
        self.mouseMoved = self.ui_wrapper.mouseMoved

        # Connect the signals to slots
        self.mousePressed.connect(self.handleMousePressed)
        self.mouseMoved.connect(self.handleMouseMoved)

    def handleMousePressed(self, globalPos):
        self.dragPos = globalPos - self.frameGeometry().topLeft()

    def handleMouseMoved(self, globalPos):
        self.move(globalPos - self.dragPos)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
