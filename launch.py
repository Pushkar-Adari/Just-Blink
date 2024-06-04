import sys
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from app_ui import Ui_Home
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        plt.style.use('theme.mplstyle')
        fig = Figure()
        self.axes = fig.add_subplot(111)
        super(MyMplCanvas, self).__init__(fig)
        self.setParent(parent)
        self.plot()
    # def __init__(self, parent=None):
    #     fig = Figure(facecolor='none')
    #     self.axes = fig.add_subplot(111,facecolor='none')
    #     super(MyMplCanvas, self).__init__(fig)
    #     self.setParent(parent)
    #     self.plot()
        
    def plot(self):
        self.axes.plot([1, 2, 3, 4, 5], [1, 2, 3, 2, 1])

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
        self.setFixedSize(800, 605)
        self.dragPos = QPoint()

        self.ui_wrapper = Ui_HomeWrapper(self)
        self.ui_wrapper.setupUi(self)
        
        self.graph_layout = QVBoxLayout(self.ui_wrapper.ui.Graph)
        self.ui_wrapper.ui.Graph.setLayout(self.graph_layout)
        self.canvas = MyMplCanvas(self.ui_wrapper.ui.Graph)
        self.graph_layout.addWidget(self.canvas)     
        self.mousePressed = self.ui_wrapper.mousePressed
        self.mouseMoved = self.ui_wrapper.mouseMoved

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