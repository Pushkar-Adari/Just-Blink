import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QBitmap, QPainter, QIcon, QCursor
from PyQt5.QtCore import Qt, QRect, QPoint, QTimer, QElapsedTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.colors import LinearSegmentedColormap
from cvzone.FaceMeshModule import FaceMeshDetector
import rc_rc


class BlinkDetectorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Just Blink")
        self.setGeometry(100, 100, 800, 605)
        self.setFixedSize(800, 605)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.initUI()
        self.initBlinkDetector()

        self.dragPos = QPoint()

    def initUI(self):
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.initTitleBar()
        self.initMainContent()
        self.initGraph()
        self.initTimers()

    def initTitleBar(self):
        self.title_bar = QtWidgets.QFrame(self.central_widget)
        self.title_bar.setFixedHeight(36)
        self.title_bar.setStyleSheet("QFrame{background-color: rgba(1, 1, 1, 1);border-bottom:1px solid #4C4C4C; border-top-left-radius: 20px; border-top-right-radius: 20px;}")
        self.layout.addWidget(self.title_bar)

        self.close_button = QtWidgets.QPushButton(self.title_bar)
        self.close_button.setGeometry(QtCore.QRect(771, 7, 22, 22))
        self.close_button.setStyleSheet("QPushButton{background-color: rgb(48, 48, 48);border-radius:10px;}QPushButton:hover{background-color: rgb(255, 0, 0);}")
        self.close_button.clicked.connect(self.close)
        self.close_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.minimize_button = QtWidgets.QPushButton(self.title_bar)
        self.minimize_button.setGeometry(QtCore.QRect(742, 7, 22, 22))
        self.minimize_button.setStyleSheet("QPushButton{background-color: rgb(48, 48, 48);border-radius:10px;}QPushButton:hover{background-color: rgb(0, 102, 255);}")
        self.minimize_button.clicked.connect(self.showMinimized)
        self.minimize_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.title_label = QtWidgets.QLabel(self.title_bar)
        self.title_label.setGeometry(QtCore.QRect(321, 0, 159, 36))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet("QLabel{color:white;}")
        self.title_label.setText("Just Blink")
        self.title_label.setAlignment(Qt.AlignCenter)

    def initMainContent(self):
        self.main_content = QtWidgets.QWidget(self.central_widget)
        self.layout.addWidget(self.main_content)

        self.start_stop_button = QtWidgets.QPushButton(self.main_content)
        self.start_stop_button.setEnabled(True)
        self.start_stop_button.setGeometry(QtCore.QRect(502, 355, 267, 82))
        font = QtGui.QFont()
        font.setFamily("Poppins SemiBold")
        font.setPointSize(15)
        self.start_stop_button.setFont(font)
        self.start_stop_button.setStyleSheet("QPushButton{background-color: rgba(1,50,32,0.5);border-radius:20;color: rgb(10,255,35);}QPushButton:checked{background-color: rgba(43, 11, 11,0.5);border-radius:20;color: rgb(249,35,35);}")
        self.start_stop_button.setCheckable(True)
        self.start_stop_button.setObjectName("StartStop")
        self.start_stop_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.start_stop_button.clicked.connect(self.toggle_blink_detection)

        self.logo_label = QtWidgets.QLabel(self.main_content)
        self.logo_label.setGeometry(QtCore.QRect(50, 28, 207, 55))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(24)
        font.setBold(True)
        self.logo_label.setFont(font)
        self.logo_label.setStyleSheet("color:white;background-color: rgba(255, 255, 255, 0);")
        self.logo_label.setText("Just Blink")

        self.avg_frame = QtWidgets.QFrame(self.main_content)
        self.avg_frame.setGeometry(QtCore.QRect(502, 108, 267, 111))
        self.avg_frame.setStyleSheet("background-color: rgba(19, 19, 19, 0.7);border-radius:20px;")
        self.avg_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.avg_frame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.avg_label = QtWidgets.QLabel(self.avg_frame)
        self.avg_label.setGeometry(QtCore.QRect(0, 0, 263, 61))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(14)
        font.setItalic(True)
        self.avg_label.setFont(font)
        self.avg_label.setStyleSheet("color:white;")
        self.avg_label.setAlignment(QtCore.Qt.AlignCenter)
        self.avg_label.setText("Average Blinks:")

        self.avg_blinks_label = QtWidgets.QLabel(self.avg_frame)
        self.avg_blinks_label.setGeometry(QtCore.QRect(0, 61, 263, 41))
        font = QtGui.QFont()
        font.setFamily("Poppins SemiBold")
        font.setPointSize(24)
        self.avg_blinks_label.setFont(font)
        self.avg_blinks_label.setStyleSheet("color:white;")
        self.avg_blinks_label.setAlignment(QtCore.Qt.AlignCenter)

    def initGraph(self):
        self.graph_frame = QtWidgets.QFrame(self.main_content)
        self.graph_frame.setGeometry(QtCore.QRect(31, 108, 458, 329))
        self.graph_frame.setStyleSheet("QFrame{background-color: rgba(19, 19, 19,0.7);border-radius:20px;}QFrame *{background-color:transparent;}")
        self.graph_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.graph_frame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.graph_layout = QVBoxLayout(self.graph_frame)
        self.graph_canvas = MyMplCanvas(self.graph_frame)
        self.graph_layout.addWidget(self.graph_canvas)

    def initTimers(self):
        self.main_timer = QTimer(self)
        self.main_timer.setInterval(1000)
        self.main_timer.timeout.connect(self.update_progress)

        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.update_frame)

        self.elapsed_timer = QElapsedTimer()

    def initBlinkDetector(self):
        self.cap = cv2.VideoCapture(0)
        self.detector = FaceMeshDetector(maxFaces=1)
        self.idlist = [22, 23, 24, 26, 110, 130, 157, 158, 159, 160, 161, 243]
        self.ratioList = []
        self.blinkCount = 0
        self.counter = 0

    def toggle_blink_detection(self):
        if self.start_stop_button.isChecked():
            self.start_detection()
        else:
            self.stop_detection()

    def start_detection(self):
        self.blinkCount = 0
        self.counter = 0
        self.ratioList = []
        self.elapsed_timer.start()
        self.blink_timer.start(30)

    def stop_detection(self):
        self.blink_timer.stop()

    def update_frame(self):
        success, img = self.cap.read()
        if not success:
            return

        img, faces = self.detector.findFaceMesh(img, draw=False)
        if faces:
            face = faces[0]
            eyeTop = face[159]
            eyeBot = face[23]
            eyeLeft = face[130]
            eyeRight = face[243]
            eyeLength, _ = self.detector.findDistance(eyeTop, eyeBot)
            eyeWidth, _ = self.detector.findDistance(eyeLeft, eyeRight)
            ratio = (eyeLength / eyeWidth) * 100
            self.ratioList.append(ratio)
            if len(self.ratioList) > 7:
                self.ratioList.pop(0)
            avgRatio = sum(self.ratioList) / len(self.ratioList)
            dynamic_limit = avgRatio * 0.9
            if ratio < dynamic_limit and self.counter == 0:
                self.blinkCount += 1
                self.counter = 1
            if self.counter != 0:
                self.counter += 1
                if self.counter > 10:
                    self.counter = 0

            elapsed_time_sec = self.elapsed_timer.elapsed() / 1000
            elapsed_time_min = elapsed_time_sec / 60
            if elapsed_time_min > 0:
                avg_blinks_per_min = self.blinkCount / elapsed_time_min
                self.avg_blinks_label.setText(f"{avg_blinks_per_min:.2f}")

    def update_progress(self):
        pass

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)

    def closeEvent(self, event):
        self.cap.release()
        cv2.destroyAllWindows()
        event.accept()


class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        super(MyMplCanvas, self).__init__(fig)
        self.setParent(parent)
        self.plot()

    def plot(self):
        self.axes.clear()
        days = ["TU", "WE", "TH", "FR", "SA", "SU", "MO", "T2"]
        values = [16, 20, 21, 22, 23, 18, 23, 26]
        bar_width = 0.55
        for i, value in enumerate(values):
            self.gradient_rect(i, 0, bar_width, value, '#8B5CA3', '#54427C')
        xtick_positions = np.arange(len(days)) + bar_width / 2
        self.axes.set_xticks(xtick_positions)
        self.axes.set_xticklabels([day[0] for day in days])
        self.axes.set_xlim(-0.5, len(days) - 0.5)
        self.axes.set_ylabel('Average', fontstyle='italic', color='darkgrey')
        self.axes.axhline(y=sum(values) / len(values), color='grey', linestyle='dotted', label='Weekly average')
        self.axes.axhline(y=15, color='mediumspringgreen', linestyle='dotted', label='Healthy')
        self.draw()

    def gradient_rect(self, x, y, width, height, color1, color2):
        gradient = np.linspace(0, 1, 256).reshape(-1, 1)
        gradient = np.hstack((gradient, gradient))
        cmap = LinearSegmentedColormap.from_list("custom_gradient", [color1, color2])
        rect = self.axes.imshow(gradient, extent=(x, x + width, y, y + height), aspect='auto', cmap=cmap, interpolation='bicubic')
        rect.set_clip_path(self.axes.patch)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BlinkDetectorApp()
    window.show()
    sys.exit(app.exec_())
