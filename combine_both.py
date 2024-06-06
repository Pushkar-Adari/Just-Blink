import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QObject, QTimer, QElapsedTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QFrame, QPushButton, QToolButton, QProgressBar, QWidget
from PyQt5.QtGui import QBitmap, QPainter, QCursor, QIcon, QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
import numpy as np
import rc_rc

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
        self.axes.set_ylabel('Average', fontstyle='italic', color='darkgrey')
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
        rect = self.axes.imshow(gradient, extent=(x, x + width, y, y + height), aspect='auto', cmap=cmap, interpolation='bicubic', zorder=2)
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
        self.elapsed_timer = QElapsedTimer()
        self.timer = QTimer()

        self.graph_layout = QVBoxLayout(self.ui_wrapper.ui.Graph)
        self.ui_wrapper.ui.Graph.setLayout(self.graph_layout)
        self.canvas = MyMplCanvas(self.ui_wrapper.ui.Graph)
        self.graph_layout.addWidget(self.canvas)
        self.mousePressed = self.ui_wrapper.mousePressed
        self.mouseMoved = self.ui_wrapper.mouseMoved
        #INITIALIZE CV
        self.cap = cv2.VideoCapture(0)
        self.detector = FaceMeshDetector(maxFaces=1)
        self.idlist = [22, 23, 24, 26, 110, 130, 157, 158, 159, 160, 161, 243]
        self.ratioList = []
        self.blinkCount = 0
        self.counter = 0
        
        # Timer for updating frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # Elapsed timer
        self.elapsed_timer = QElapsedTimer()
        self.mousePressed.connect(self.handleMousePressed)
        self.mouseMoved.connect(self.handleMouseMoved)
        self.ui_wrapper.ui.StartStop.clicked.connect(self.toggle_detection)
    def handleMousePressed(self, globalPos):
        self.dragPos = globalPos - self.frameGeometry().topLeft()

    def handleMouseMoved(self, globalPos):
        self.move(globalPos - self.dragPos)

    def toggle_detection(self, checked):
        if checked:
            self.start_detection()
        else:
            self.stop_detection()

    def start_detection(self):
        self.blinkCount = 0
        self.counter = 0
        self.ratioList = []
        self.elapsed_timer.start()
        self.timer.start(30)  # Update frame every 30 ms
        
    def stop_detection(self):
        self.timer.stop()
        
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
                self.ui_wrapper.ui.AvgBlinksPerMinute.setText(f"{avg_blinks_per_min:.0f}/MIN")


class Ui_Home(object):
    mousePressed = pyqtSignal(QPoint)
    mouseMoved = pyqtSignal(QPoint)

    def setupUi(self, Home):
        #///////// VALUES ///////
        self.min50total = 3000
        self.min10total = 600
        self.min10actual = self.min10total
        self.min50actual = self.min50total

        #///////// HOME /////////
        Home.setObjectName("Home")
        Home.setFixedSize(800, 605)
        Home.setAutoFillBackground(False)
        Home.setStyleSheet("")
        Home.setAttribute(Qt.WA_TranslucentBackground, True)
        self.Central = QWidget(Home)
        self.Central.setStyleSheet("")
        self.Central.setObjectName("Central")

        #///////// CUSTOM TITLE BAR /////////
        self.TitleBar = QFrame(self.Central)
        self.TitleBar.setGeometry(0, 0, 800, 36)
        self.TitleBar.setStyleSheet("QFrame{background-color: rgba(1, 1, 1, 1);border-bottom:1px solid #4C4C4C; border-top-left-radius: 20px; border-top-right-radius: 20px;}")
        self.TitleBar.setObjectName("TitleBar")

        self.closeApp = QPushButton(self.TitleBar)
        self.closeApp.setGeometry(771, 7, 22, 22)
        self.closeApp.setStyleSheet("QPushButton{background-color: rgb(48, 48, 48);border-radius:10px;icon-size:12px;}QPushButton:hover{background-color: rgb(255, 0, 0);border-radius:10px;icon:url(:/newPrefix/assets/close.png);}")
        self.closeApp.setObjectName("closeApp")
        self.closeApp.clicked.connect(self.closeWindow)
        self.closeApp.setCursor(QCursor(Qt.PointingHandCursor))

        self.minApp = QPushButton(self.TitleBar)
        self.minApp.setGeometry(742, 7, 22, 22)
        self.minApp.setStyleSheet("QPushButton{background-color: rgb(48, 48, 48);border-radius:10px;icon-size:12px;}QPushButton:hover{background-color: rgb(0, 102, 255);border-radius:10px;icon:url(:/newPrefix/assets/min.png);}")
        self.minApp.setObjectName("minApp")
        self.minApp.clicked.connect(self.minimize_window)
        self.minApp.setCursor(QCursor(Qt.PointingHandCursor))

        self.titlelabel = QLabel(self.TitleBar)
        self.titlelabel.setGeometry(321, 0, 159, 36)
        font = QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        font.setItalic(False)
        self.titlelabel.setFont(font)
        self.titlelabel.setStyleSheet("QLabel{color:white;}")
        self.titlelabel.setText("Just Blink")
        self.titlelabel.setAlignment(Qt.AlignCenter)

        #///////// MAIN CONTENT /////////
        self.MainContent = QWidget(self.Central)
        self.MainContent.setGeometry(0, 36, 800, 569)
        self.MainContent.setObjectName("MainContent")

        #///////// START/STOP  /////////
        self.StartStop = QPushButton(self.MainContent)
        self.StartStop.setEnabled(True)
        self.StartStop.setGeometry(502, 355, 267, 82)
        font = QFont()
        font.setFamily("Poppins SemiBold")
        font.setPointSize(15)
        font.setItalic(False)
        self.StartStop.setFont(font)
        self.StartStop.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.StartStop.setStyleSheet("QPushButton{background-color: rgba(1,50,32,0.5);border-radius:20;color: rgb(10,255,35);font: 63 14.5pt \"Poppins SemiBold\";}QPushButton:checked{background-color: rgba(43, 11, 11,0.5);border-radius:20;color: rgb(249,35,35);font: 63 14.5pt \"Poppins SemiBold\";}")
        self.StartStop.setCheckable(True)
        self.StartStop.setChecked(False)
        self.StartStop.setObjectName("StartStop")
        self.StartStop.setCursor(QCursor(Qt.PointingHandCursor))

        #///////// LOGO /////////
        self.Logo = QLabel(self.MainContent)
        self.Logo.setGeometry(50, 28, 207, 55)
        font = QFont()
        font.setFamily("Poppins")
        font.setPointSize(24)
        font.setBold(True)
        font.setItalic(False)
        self.Logo.setFont(font)
        self.Logo.setStyleSheet("color:white;background-color: rgba(255, 255, 255, 0);")
        self.Logo.setObjectName("Logo")

        #///////// PROFILE /////////
        self.Profile = QToolButton(self.MainContent)
        self.Profile.setGeometry(677, 33, 43, 43)
        self.Profile.setStyleSheet("background-color: rgb(19, 19, 19);border-radius:21px;icon-size:25px;")
        icon = QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/assets/user.png"), QIcon.Normal, QIcon.Off)
        self.Profile.setIcon(icon)
        self.Profile.setObjectName("Profile")
        self.Profile.setCursor(QCursor(Qt.PointingHandCursor))

        #///////// SETTINGS /////////
        self.Setting = QToolButton(self.MainContent)
        self.Setting.setGeometry(726, 33, 44, 44)
        self.Setting.setStyleSheet("background-color: rgb(19, 19, 19);border-radius:22px;icon-size:25px;")
        icon1 = QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/newPrefix/assets/setting.png"), QIcon.Normal, QIcon.Off)
        self.Setting.setIcon(icon1)
        self.Setting.setObjectName("Setting")
        self.Setting.setCursor(QCursor(Qt.PointingHandCursor))

        #///////// AVERAGE /////////
        self.Avg = QFrame(self.MainContent)
        self.Avg.setGeometry(502, 108, 267, 111)
        self.Avg.setStyleSheet("background-color: rgba(19, 19, 19, 0.7);border-radius:20px;")
        self.Avg.setFrameShape(QFrame.StyledPanel)
        self.Avg.setFrameShadow(QFrame.Raised)
        self.Avg.setObjectName("Avg")

        self.AverageHeading = QLabel(self.Avg)
        self.AverageHeading.setGeometry(0, 0, 263, 61)
        font = QFont()
        font.setFamily("Poppins")
        font.setPointSize(14)
        font.setItalic(True)
        self.AverageHeading.setFont(font)
        self.AverageHeading.setAutoFillBackground(False)
        self.AverageHeading.setStyleSheet("background-color: rgba(255, 255, 255, 0);color:white;")
        self.AverageHeading.setAlignment(Qt.AlignCenter)
        self.AverageHeading.setObjectName("AverageHeading")

        self.AvgBlinksPerMinute = QLabel(self.Avg)
        self.AvgBlinksPerMinute.setGeometry(0, 50, 263, 41)
        font = QFont()
        font.setFamily("Poppins SemiBold")
        font.setPointSize(16)
        self.AvgBlinksPerMinute.setFont(font)
        self.AvgBlinksPerMinute.setStyleSheet("background-color: rgba(255, 255, 255, 0);color:white;")
        self.AvgBlinksPerMinute.setAlignment(Qt.AlignCenter)
        self.AvgBlinksPerMinute.setObjectName("AvgBlinksPerMinute")

        #///////// WEEKLY GROWTH /////////
        self.Week = QFrame(self.MainContent)
        self.Week.setGeometry(502, 230, 267, 111)
        self.Week.setStyleSheet("background-color: rgba(19, 19, 19, 0.7);border-radius:20px;")
        self.Week.setFrameShape(QFrame.StyledPanel)
        self.Week.setFrameShadow(QFrame.Raised)
        self.Week.setObjectName("Week")

        self.weekHeading = QLabel(self.Week)
        self.weekHeading.setGeometry(0, 0, 263, 61)
        font = QFont()
        font.setFamily("Poppins")
        font.setPointSize(14)
        font.setItalic(True)
        self.weekHeading.setFont(font)
        self.weekHeading.setStyleSheet("background-color: rgba(0,0,0,0);color:white;")
        self.weekHeading.setAlignment(Qt.AlignCenter)
        self.weekHeading.setObjectName("weekHeading")

        self.weeklyGrowth = QLabel(self.Week)
        self.weeklyGrowth.setGeometry(0, 50, 263, 41)
        font = QFont()
        font.setFamily("Poppins SemiBold")
        font.setPointSize(16)
        font.setItalic(False)
        self.weeklyGrowth.setFont(font)
        self.weeklyGrowth.setStyleSheet("background-color: rgba(0,0,0,0);color:#00FF1A;")
        self.weeklyGrowth.setAlignment(Qt.AlignCenter)
        self.weeklyGrowth.setObjectName("weeklyGrowth")

        #///////// GRAPH /////////
        self.Graph = QFrame(self.MainContent)
        self.Graph.setGeometry(31, 108, 458, 329)
        self.Graph.setStyleSheet("QFrame{background-color: rgba(19, 19, 19,0.7);border-radius:20px;}QFrame *{background-color:transparent;}")
        self.Graph.setFrameShape(QFrame.StyledPanel)
        self.Graph.setFrameShadow(QFrame.Raised)
        self.Graph.setObjectName("Graph")

        #///////// TIMER /////////
        self.TimerLabel = QLabel(self.MainContent)
        self.TimerLabel.setGeometry(43, 450, 210, 44)
        font = QFont()
        font.setFamily("Poppins")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        self.TimerLabel.setFont(font)
        self.TimerLabel.setStyleSheet("color:white;font-size: 14.5pt;background-color: rgba(0, 0, 0, 0);")
        self.TimerLabel.setFrameShape(QFrame.NoFrame)
        self.TimerLabel.setFrameShadow(QFrame.Plain)
        self.TimerLabel.setWordWrap(False)
        self.TimerLabel.setObjectName("TimerLabel")

        self.Pause = QToolButton(self.MainContent)
        self.Pause.setGeometry(678, 498, 43, 43)
        self.Pause.setStyleSheet("background-color: rgb(19, 19, 19);border-radius:21px;icon-size:20px;")
        icon2 = QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/newPrefix/assets/play.png"), QIcon.Normal, QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(":/newPrefix/assets/pause.png"), QIcon.Normal, QIcon.On)
        self.Pause.setIcon(icon2)
        self.Pause.setCheckable(True)
        self.Pause.setChecked(False)
        self.Pause.setObjectName("Pause")
        self.Pause.setCursor(QCursor(Qt.PointingHandCursor))
        self.Pause.toggled.connect(self.toggle_timer)

        self.Reset = QToolButton(self.MainContent)
        self.Reset.setGeometry(726, 498, 43, 43)
        self.Reset.setStyleSheet("background-color: rgb(19, 19, 19);border-radius:21px;icon-size:20px;")
        icon3 = QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/newPrefix/assets/reset.png"), QIcon.Normal, QIcon.Off)
        self.Reset.setIcon(icon3)
        self.Reset.setObjectName("Reset")
        self.Reset.clicked.connect(self.reset_timer)
        self.Reset.setCursor(QCursor(Qt.PointingHandCursor))

        self.Name = QFrame(self.MainContent)
        self.Name.setGeometry(586, 38, 119, 32)
        self.Name.setStyleSheet("background-color: rgba(19, 19, 19, 0.7);border-radius:15px;")
        self.Name.setFrameShape(QFrame.StyledPanel)
        self.Name.setFrameShadow(QFrame.Raised)
        self.Name.setObjectName("Name")

        self.Background = QFrame(self.MainContent)
        self.Background.setGeometry(0, 0, 800, 569)
        self.Background.setStyleSheet("border-image: url(:/newPrefix/b2.png) 0 0 0 0 stretch stretch;border-width: 0px;border-bottom-left-radius: 30px; border-bottom-right-radius: 30px;")
        self.Background.setFrameShape(QFrame.StyledPanel)
        self.Background.setFrameShadow(QFrame.Raised)
        self.Background.setObjectName("Background")

        #///////// PROGRESS BARS /////////
        self.min10 = QProgressBar(self.MainContent)
        self.min10.setGeometry(32, 498, 106, 43)
        self.min10.setStyleSheet("QProgressBar{background-color:rgba(45,45,45,0.5);border-radius:21px;text-align:center;color:transparent;}QProgressBar::chunk{background:qLineargradient(spread:pad, x1:0, y1:0, x2:1, x2:1, stop:0 rgba(52,30,63,255),stop:1 rgba(134,89,157,255));border-radius:21px;}")
        self.min10.setRange(0, self.min10total)
        self.min10.setValue(self.min10actual)
        self.min10.setObjectName("min10")
        bm = QBitmap(self.min10.size())
        bm.fill(Qt.color0)
        p = QPainter(bm)
        p.setRenderHint(QPainter.HighQualityAntialiasing)
        p.setPen(Qt.color1)
        p.setBrush(Qt.color1)
        radius = 21
        p.drawRoundedRect(0, 0, bm.width(), bm.height(), radius, radius)
        p.end()
        self.min10.setMask(bm)
        self.min10label = QLabel(self.MainContent)
        self.min10label.setGeometry(32, 498, 106, 43)
        font = QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        font.setItalic(False)
        self.min10label.setFont(font)
        self.min10label.setStyleSheet("QLabel{color:white;}")
        self.min10label.setText("10m00s")
        self.min10label.setAlignment(Qt.AlignCenter)

        self.min50 = QProgressBar(self.MainContent)
        self.min50.setGeometry(143, 498, 530, 43)
        self.min50.setStyleSheet("QProgressBar{background-color:rgba(45,45,45,0.5);border-radius:21px;text-align:center;color:transparent;}QProgressBar::chunk{background:qLineargradient(spread:pad, x1:0, y1:0, x2:1, x2:1, stop:0 rgba(2,19,51,255),stop:1 rgba(50,51,113,255));border-radius:21px;}")
        self.min50.setRange(0, self.min50total)
        self.min50.setValue(self.min50total)
        self.min50.setObjectName("min50")
        bm = QBitmap(self.min50.size())
        bm.fill(Qt.color0)
        p = QPainter(bm)
        p.setRenderHint(QPainter.HighQualityAntialiasing)
        p.setPen(Qt.color1)
        p.setBrush(Qt.color1)
        radius = 21
        p.drawRoundedRect(0, 0, bm.width(), bm.height(), radius, radius)
        p.end()
        self.min50.setMask(bm)
        self.min50label = QLabel(self.MainContent)
        self.min50label.setGeometry(143, 498, 530, 43)
        font = QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        font.setItalic(False)
        self.min50label.setFont(font)
        self.min50label.setStyleSheet("QLabel{color:white;}")
        self.min50label.setText("50m00s")
        self.min50label.setAlignment(Qt.AlignCenter)

        self.Background.raise_()
        self.Name.raise_()
        self.StartStop.raise_()
        self.Logo.raise_()
        self.Setting.raise_()
        self.Avg.raise_()
        self.Week.raise_()
        self.Graph.raise_()
        self.TimerLabel.raise_()
        self.Pause.raise_()
        self.Reset.raise_()
        self.Profile.raise_()
        self.min10.raise_()
        self.min50.raise_()
        self.min10label.raise_()
        self.min50label.raise_()
        Home.setCentralWidget(self.Central)

        self.retranslateUi(Home)
        QtCore.QMetaObject.connectSlotsByName(Home)

        #///////// TIMER SETUP /////////
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_progress)

    def retranslateUi(self, Home):
        _translate = QtCore.QCoreApplication.translate
        Home.setWindowTitle(_translate("Home", "Just Blink"))
        self.StartStop.setText(_translate("Home", "Stop Tracking"))
        self.Logo.setText(_translate("Home", "Just Blink"))
        self.Profile.setText(_translate("Home", "..."))
        self.Setting.setText(_translate("Home", "..."))
        self.AverageHeading.setText(_translate("Home", "Average Blinks:"))
        self.AvgBlinksPerMinute.setText(_translate("Home", "Not active"))

        self.weekHeading.setText(_translate("Home", "Weekly Report :"))
        self.weeklyGrowth.setText(_translate("Home", "40%"))
        self.TimerLabel.setText(_translate("Home", "Pomodoro Timer"))
        self.Pause.setText(_translate("Home", "..."))
        self.Reset.setText(_translate("Home", "..."))

    #///////// FUNCTIONALITY /////////
    def changePlayIcon(self):
        if self.Pause.icon().name() == "play.png":
            self.Pause.setIcon(QIcon(":/newPrefix/assets/pause.png"))
        else:
            self.Pause.setIcon(QIcon(":/newPrefix/assets/play.png"))

    def toggle_timer(self, checked):
        if checked:
            self.timer.start()
            self.Pause.setIcon(QIcon(":/newPrefix/assets/pause.png"))
        else:
            self.timer.stop()
            self.Pause.setIcon(QIcon(":/newPrefix/assets/play.png"))

    def update_progress(self):
        self.min50actual -= 1
        self.min50.setValue(self.min50actual)
        if self.min50actual <= 0:
            self.update_restProgress()
        self.min50label.setText(self.update_min50_time())

    def update_restProgress(self):
        self.min10actual -= 1
        self.min10.setValue(self.min10actual)
        if self.min10actual <= 0:
            self.reset_timer()
        self.min10label.setText(self.update_min10_time())

    def reset_timer(self):
        self.timer.stop()
        self.min50actual = self.min50total
        self.min50.setValue(self.min50actual)
        self.min10actual = self.min10total
        self.min10.setValue(self.min10actual)
        self.Pause.setChecked(False)
        self.min50label.setText("50m00s")
        self.min10label.setText("10m00s")

    def update_min50_time(self):
        if self.min50actual > 0:
            self.min50time = f"{self.min50actual//60:02}m{self.min50actual%60:02}s"
            return self.min50time
        self.min50time = "00m00s"
        return self.min50time

    def update_min10_time(self):
        if self.min10actual > 0:
            self.min10time = f"{self.min10actual//60:02}m{self.min10actual%60:02}s"
            return self.min10time
        self.min10time = "00m00s"
        return self.min10time

    def minimize_window(self):
        self.MainContent.window().showMinimized()

    def closeWindow(self):
        self.MainContent.window().close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mousePressed.emit(event.globalPos())

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.mouseMoved.emit(event.globalPos())
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())