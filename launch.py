import sys
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QObject, QTimer, QElapsedTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from app_ui import Ui_Home
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
import numpy as np

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        plt.style.use('theme.mplstyle')
        fig = Figure()
        self.axes = fig.add_subplot(111)
        super(MyMplCanvas, self).__init__(fig)
        self.setParent(parent)
        self.plot()

    def plot(self):
        self.axes.clear()
        days = ["TU","WE","TH","FR","SA","SU","MO","T2"]
        values = [16, 20, 21, 22, 23, 18, 23, 26]
        bar_width = 0.55
        for i, value in enumerate(values):
            self.gradient_rect(i, 0, bar_width, value, '#8B5CA3', '#54427C')
        xtick_positions = np.arange(len(days)) + bar_width / 2
        self.axes.set_xticks(xtick_positions)
        xticklabels = [day[0] for day in days]
        self.axes.set_xticklabels(xticklabels)
        yticks = self.axes.get_yticks()
        yticks = ['' if tick == 0 else f'{int(tick)}' for tick in yticks]
        self.axes.set_yticklabels(yticks, ha='center')
        self.axes.set_yticklabels(yticks)
        self.axes.set_xlim(-0.5, len(days) - 0.5)
        self.axes.set_ylabel('Average',fontstyle='italic',color='darkgrey')
        self.customize_zorder()
        average_value = sum(values) / len(values)
        avgweek = self.axes.axhline(y=average_value, color='grey', linestyle='dotted', label = 'Weekly average')
        goodavg = self.axes.axhline(y=15, color='mediumspringgreen', linestyle='dotted', label = 'Healthy')
        goodavg.set_zorder(1)
        avgweek.set_zorder(1)
        self.draw()

    def gradient_rect(self, x, y, width, height, color1, color2):
        gradient = np.linspace(0, 1, 256).reshape(-1, 1)
        gradient = np.hstack((gradient, gradient))
        cmap = LinearSegmentedColormap.from_list("custom_gradient", [color1, color2])
        rect = self.axes.imshow(gradient, extent=(x, x + width, y, y + height), aspect='auto', cmap=cmap, interpolation='bicubic',zorder=2)
        rect.set_clip_path(self.axes.patch)
    def customize_zorder(self):
        self.axes.set_zorder(3)
        self.axes.grid(True, which='minor', linestyle='-', zorder=1)

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
