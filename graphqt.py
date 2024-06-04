import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(facecolor='none')
        self.axes = fig.add_subplot(111,facecolor='none')
        super(MyMplCanvas, self).__init__(fig)
        self.setParent(parent)
        self.plot()

    def plot(self):
        # Add your plot code here. For example:
        self.axes.plot([1, 2, 3, 4, 5], [1, 2, 3, 2, 1])

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.widget = QWidget()
        self.widget.setStyleSheet("background-color:green;")
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)
        self.canvas = MyMplCanvas(self.widget)
        self.layout.addWidget(self.canvas)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
