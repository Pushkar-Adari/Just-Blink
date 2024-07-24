import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QObject, QTimer, QElapsedTimer, QCoreApplication, QSettings
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout,QDialog, QLabel, QFrame, QPushButton, QToolButton, QProgressBar, QWidget, QSlider, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QBitmap, QPainter, QCursor, QIcon, QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from qtwidgets import AnimatedToggle
from plyer import notification
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import time
from matplotlib.colors import LinearSegmentedColormap
import cv2
import cvzone
import csv
from cvzone.FaceMeshModule import FaceMeshDetector
import numpy as np
import rc_rc
import threading

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        plt.style.use('theme.mplstyle')
        fig = Figure()
        self.axes = fig.add_subplot(111)
        super(MyMplCanvas, self).__init__(fig)
        self.setParent(parent)
        self.ui_wrapper = Ui_HomeWrapper(self)  
        self.plot()
    def createCSV(self,file_path):
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        if not os.path.exists(file_path):
            with open(file_path, 'w', newline='') as file:
                fieldnames = ['date', 'day', 'average_blinks']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                
                for i in range(7):
                    date = datetime.now() - timedelta(days=i)
                    writer.writerow({
                        'date': date.strftime('%Y-%m-%d'),
                        'day': date.strftime('%A'),
                        'average_blinks': 1
                    })
    def get_data_from_csv(self):
        data = []
        file_path = 'Profiles/User/data.csv'
        self.createCSV(file_path)

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
            data = data[-7:]
            days = [entry['day'] for entry in data]
            values = [int(entry['average_blinks']) for entry in data]
        return days, values
    
    def plot(self):
        self.axes.clear()
        days, values = self.get_data_from_csv()
        bar_width = 0.5
        for i, value in enumerate(values):
            self.gradient_rect(i, 0, bar_width, value, '#8B5CA3', '#54427C')
        xtick_positions = np.arange(len(days)) + bar_width / 2
        self.axes.set_xticks(xtick_positions)
        xticklabels = [day[0] for day in days]
        self.axes.set_xticklabels(xticklabels)
        yticks = [0, 5, 10, 15, 20, 25, 30]
        yticks = ['' if tick == 0 else f'{int(tick)}' for tick in yticks] #Make space for 0 but hide it cuz ugly
        self.axes.set_yticklabels(yticks, ha='center')
        self.axes.set_xlim(-0.5, len(days) - 0.5)
        self.axes.set_ylim(0, 25)
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
        self.get_data_from_csv()
        self.update_weekly_report()
        self.graph_layout = QVBoxLayout(self.ui_wrapper.ui.Graph)
        self.ui_wrapper.ui.Graph.setLayout(self.graph_layout)
        self.canvas = MyMplCanvas(self.ui_wrapper.ui.Graph)
        self.graph_layout.addWidget(self.canvas)
        self.mousePressed = self.ui_wrapper.mousePressed
        self.mouseMoved = self.ui_wrapper.mouseMoved
        self.ui_wrapper.ui.settingconf.setValue('noti_int',180)
        self.min_notification_interval = int(self.ui_wrapper.ui.settingconf.value('noti_int',180))
        self.avg_blinks_per_min = 16

        self.notification_thread = threading.Thread(target=self.send_blink_reminder)
        self.notification_thread.daemon = True  # so the thread dies when the main program dies
        self.notification_thread.start()
        #INITIALIZE CV
        self.cap = cv2.VideoCapture(0)
        self.detector = FaceMeshDetector(maxFaces=1)
        self.idlist = [22, 23, 24, 26, 110, 130, 157, 158, 159, 160, 161, 243]
        self.ratioList = []
        self.blinkCount = 0
        self.counter = 0
        
        #System tray Menu

        self.appIcon = QIcon("assets/logos/48x48.ico")
        self.trayIco = QSystemTrayIcon(self)
        self.trayIco.setIcon(self.appIcon)
        self.trayIco.setVisible(True)
        self.trayMenu = QMenu(self)
        self.trayMenu.setStyleSheet("""
        QMenu{
            background-color:transparent;
            color:white;
            border-radius:0px;
            font-family: Poppins;
            width:146px;
            height:152px;
        }
        QMenu::item{
            background-color:#000;
            padding: 5px 20px;
            border: 1px solid transparent;
        }
        QMenu::item:selected{
            background-color: #4A4A4A;
            border: 1px solid #888;
        }
        
        
    """)        
        op1 = QAction("Show app",self)
        op1.triggered.connect(lambda:self.ui_wrapper.ui.MainContent.window().show())
        op2 = QAction("Start Tracking",self)
        op2.triggered.connect(lambda:self.toggle_detection(True))
        op3 = QAction("Stop Tracking",self)
        op3.triggered.connect(lambda:self.toggle_detection(False))
        op4 = QAction("Quit",self)
        op4.triggered.connect(lambda:self.ui_wrapper.ui.MainContent.window().close())


        self.trayMenu.addAction(op1)
        self.trayMenu.addAction(op2)
        self.trayMenu.addAction(op3)
        self.trayMenu.addAction(op4)
        
        self.trayIco.setContextMenu(self.trayMenu)

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
            self.ui_wrapper.ui.StartStop.setChecked(True)
            self.ui_wrapper.ui.StartStop.setText("Starting...")
            QCoreApplication.processEvents()
            self.start_detection()
        else:
            self.ui_wrapper.ui.StartStop.setChecked(False) #Because calling toggle function from tray menu doesn't change button state
            self.ui_wrapper.ui.StartStop.setText("Start Tracking")
            self.stop_detection()

    def start_detection(self):
        self.cap = cv2.VideoCapture(0)
        self.blinkCount = 0
        self.counter = 0
        self.ratioList = []
        self.elapsed_timer.start()
        self.timer.start(30)  # Update frame every 30 ms
        self.ui_wrapper.ui.StartStop.setText("Stop Tracking")
        start_reminder = notification.notify(
            title = '',
            message = 'Just Blink has started Tracking',
            app_icon = None,
            timeout = 10,
            toast = False
        )
    def createCSV(self,file_path):
        if not os.path.exists(file_path):
            with open(file_path, 'w', newline='') as file:
                fieldnames = ['date', 'day', 'average_blinks']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                
                for i in range(9,-1,-1):
                    date = datetime.now() - timedelta(days=i)
                    writer.writerow({
                        'date': date.strftime('%Y-%m-%d'),
                        'day': date.strftime('%A'),
                        'average_blinks': 1
                    })
    def get_data_from_csv(self):
        data = []
        file_path = 'Profiles/User/data.csv'
        self.createCSV(file_path)
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
            data = data[-7:]
            days = [entry['day'] for entry in data]
            values = [int(entry['average_blinks']) for entry in data]
        return days, values
    def update_weekly_report(self):
        days, values = self.get_data_from_csv()
        last_7_days = values[-7:]
    
        valid_values = [value for value in last_7_days if value != 1]
        
        if len(valid_values) < 2:
            growth = 0
        else:
            yesterday = valid_values[-1]
            weekago = valid_values[0]
            growth = ((yesterday - weekago) / weekago) * 100
        if growth > 0:
            self.ui_wrapper.ui.weeklyGrowth.setText(f"+{growth:.1f}%")
        elif growth < 0:
            self.ui_wrapper.ui.weeklyGrowth.setText(f"{growth:.1f}%")
            self.ui_wrapper.ui.weeklyGrowth.setStyleSheet("background-color: rgba(0,0,0,0);color:rgb(249,35,35);")
        elif growth == 0:
            self.ui_wrapper.ui.weeklyGrowth.setText(f"{growth:.1f}%")
            self.ui_wrapper.ui.weeklyGrowth.setStyleSheet("background-color: rgba(0,0,0,0);color:rgb(255,255,255);")



        
    

    
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
            dynamic_limit = avgRatio * float(self.ui_wrapper.ui.settingconf.value('SensValue',0.9))

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
                self.avg_blinks_per_min = self.blinkCount / elapsed_time_min
                self.ui_wrapper.ui.AvgBlinksPerMinute.setText(f"{self.avg_blinks_per_min:.0f}/MIN")
            
        
    def send_blink_reminder(self):
        while True:
            try:
                if self.avg_blinks_per_min <= 15:
                    notification.notify(
                    title = '',
                    message = "You haven't blinked in a while!",
                    app_icon = None,
                    timeout = 10,
                    toast = False
                    )
                time.sleep(self.min_notification_interval)
            except Exception as e:
                print(f"An error occurred: {e}")
    def save_blinks_to_csv(self):
        file_path = 'Profiles/User/data.csv'
        today = datetime.today().strftime('%Y-%m-%d')
        day = datetime.today().strftime('%A')
        new_entry = {'date': today, 'day': day, 'average_blinks': int(self.avg_blinks_per_min)}
        entries = []
        try:
            with open(file_path, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    entries.append(row)
        except FileNotFoundError:
            pass
        
        # Check if today's entry exists and update it
        entry_exists = False
        for entry in entries:
            if entry['date'] == today:
                entry['day'] = day
                entry['average_blinks'] = new_entry['average_blinks']
                entry_exists = True
                break
        if not entry_exists:
            entries.append(new_entry)
        with open(file_path, 'w', newline='') as file:
            fieldnames = ['date', 'day', 'average_blinks']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(entries)
    def stop_detection(self):
        
        self.timer.stop()
        self.cap.release()
        notification.notify(
            title = '',
            message = 'Just Blink has stopped Tracking',
            app_icon = None,
            timeout = 10,
            toast = False
            
        )
        self.save_blinks_to_csv()
        self.avg_blinks_per_min = 16



class Ui_Home(object):
    mousePressed = pyqtSignal(QPoint)
    mouseMoved = pyqtSignal(QPoint)

    def setupUi(self, Home):

        self.Home = Home
        self.settingconf = QSettings("JustBlink")
        #///////// VALUES ///////
        self.min50total = int(self.settingconf.value("min50total",3000))
        self.min10total = int(self.settingconf.value("min10total",600))


        self.min10actual = self.min10total
        self.min50actual = self.min50total

        #///////// HOME /////////
        Home.setObjectName("Home")
        Home.setFixedSize(800, 605)
        Home.setAutoFillBackground(False)
        Home.setAttribute(Qt.WA_TranslucentBackground, True)
        self.Central = QWidget(Home)
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
        self.StartStop.setStyleSheet("QPushButton{background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,stop:0 rgba(1, 173, 59, 0.3),stop:1 rgba(1, 50, 32, 0.3));border-radius:20;color: rgb(10,255,35);font: 63 14.5pt \"Poppins SemiBold\";}QPushButton:checked{background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,stop:0 rgba(64, 16, 16, 0.3),stop:1 rgba(184, 19, 19, 0.3));border-radius:20;color: rgb(249,35,35);font: 63 14.5pt \"Poppins SemiBold\";}")
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


        #///////// SETTINGS /////////
        self.Setting = QToolButton(self.MainContent)
        self.Setting.setGeometry(726, 33, 44, 44)
        self.Setting.setStyleSheet("background-color: rgb(19, 19, 19);border-radius:22px;icon-size:25px;")
        icon1 = QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/newPrefix/assets/setting.png"), QIcon.Normal, QIcon.Off)
        self.Setting.setIcon(icon1)
        self.Setting.setObjectName("Setting")
        self.Setting.setCursor(QCursor(Qt.PointingHandCursor))
        self.Setting.clicked.connect(self.OpenSettings)

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
        
        self.PomodoroInfo = QPushButton(self.MainContent)
        self.PomodoroInfo.setGeometry(257, 459, 20, 20)
        info = QIcon()
        info.addPixmap(QtGui.QPixmap(":/newPrefix/assets/info.png"), QIcon.Normal, QIcon.Off)
        self.PomodoroInfo.setIcon(info)
        self.PomodoroInfo.setStyleSheet("background-color: #2D2D2D;border-radius:10px;icon-size:16px;")
        self.PomodoroInfo.setObjectName("PomodoroInfo")
        self.PomodoroInfo.setCursor(QCursor(Qt.PointingHandCursor))
        self.PomodoroInfo.enterEvent = self.showPInfo
        self.PomodoroInfo.leaveEvent = self.hidePInfo
        
        self.PomodoroInfoText = QLabel(self.MainContent)
        self.PomodoroInfoText.setGeometry(280, 417, 275, 80)
        font = QFont()
        font.setFamily("Poppins Light")
        font.setBold(False)
        font.setItalic(False)
        self.PomodoroInfoText.setFont(font)
        self.PomodoroInfoText.setStyleSheet("color:white;font-size: 8.5pt;background-color: rgba(0,0,0,0);border-radius:14px;")
        self.PomodoroInfoText.setFrameShape(QFrame.NoFrame)
        self.PomodoroInfoText.setFrameShadow(QFrame.Plain)
        self.PomodoroInfoText.setWordWrap(True)
        self.PomodoroInfoText.setObjectName("PomodoroInfoText")
        
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

        # self.Name = QFrame(self.MainContent)
        # self.Name.setGeometry(586, 38, 119, 32)
        # self.Name.setStyleSheet("background-color: rgba(19, 19, 19, 0.7);border-radius:15px;")
        # self.Name.setFrameShape(QFrame.StyledPanel)
        # self.Name.setFrameShadow(QFrame.Raised)
        # self.Name.setObjectName("Name")

        self.Background = QFrame(self.MainContent)
        self.Background.setGeometry(0, 0, 800, 569)
        self.Background.setStyleSheet("border-image: url(:/newPrefix/b2.png) 0 0 0 0 stretch stretch;border-width: 0px;border-bottom-left-radius: 30px; border-bottom-right-radius: 30px;")
        self.Background.setFrameShape(QFrame.StyledPanel)
        self.Background.setFrameShadow(QFrame.Raised)
        self.Background.setObjectName("Background")

        #///////// PROGRESS BARS /////////
        self.min10 = QProgressBar(self.MainContent)
        self.min10.setGeometry(32, 498, 106, 43)
        self.min10.setStyleSheet("QProgressBar{background-color:rgba(45,45,45,0.5);border-radius:21px;text-align:center;color:transparent;}QProgressBar::chunk{background:qLineargradient(spread:pad, x1:0, y1:0, x2:1, x2:1, stop:0 rgba(202,105,198,255),stop:1 rgba(134,89,157,255));border-radius:21px;}")
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
        self.min10label.setText(self.settingconf.value("min10label","10m00s"))
        self.min10label.setAlignment(Qt.AlignCenter)

        self.min50 = QProgressBar(self.MainContent)
        self.min50.setGeometry(143, 498, 530, 43)
        self.min50.setStyleSheet("QProgressBar{background-color:rgba(45,45,45,0.5);border-radius:21px;text-align:center;color:transparent;}QProgressBar::chunk{background:qLineargradient(spread:pad, x1:0, y1:0, x2:1, x2:1, stop:0 #4E397A,stop:1 #D391F3);border-radius:21px;}")
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
        self.min50label.setText(self.settingconf.value("min50label","50m00s"))
        self.min50label.setAlignment(Qt.AlignCenter)

        self.Background.raise_()
        self.StartStop.raise_()
        self.Logo.raise_()
        self.Setting.raise_()
        self.Avg.raise_()
        self.Week.raise_()
        self.Graph.raise_()
        self.TimerLabel.raise_()
        self.Pause.raise_()
        self.Reset.raise_()
        self.min10.raise_()
        self.min50.raise_()
        self.min10label.raise_()
        self.min50label.raise_()
        self.PomodoroInfo.raise_()
        self.PomodoroInfoText.raise_()
        Home.setCentralWidget(self.Central)

        self.retranslateUi(Home)
        QtCore.QMetaObject.connectSlotsByName(Home)

        #///////// TIMER SETUP /////////
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_progress)

    def showPInfo(self,event):
        time.sleep(0.3)
        self.PomodoroInfoText.setText('Divide your work into intervals with breaks to boost productivity.\nChange session length in settings.')
        self.PomodoroInfoText.setStyleSheet("color:white;font-size: 8.5pt;background-color: #181818;border-radius:14px;text-align: center;padding:5px;")

    def hidePInfo(self,event):
        self.PomodoroInfoText.setText('')
        self.PomodoroInfoText.setStyleSheet("color:white;font-size: 8.5pt;background-color: rgba(0,0,0,0);border-radius:14px;")



    def retranslateUi(self, Home):
        _translate = QtCore.QCoreApplication.translate
        Home.setWindowTitle(_translate("Home", "Just Blink"))

        self.Logo.setText(_translate("Home", "Just Blink"))
        self.Setting.setText(_translate("Home", "..."))
        self.AverageHeading.setText(_translate("Home", "Average Blinks:"))
        self.AvgBlinksPerMinute.setText(_translate("Home", "Not active"))

        self.weekHeading.setText(_translate("Home", "Weekly Report :"))
        self.weeklyGrowth.setText(_translate("Home", "00%"))
        self.TimerLabel.setText(_translate("Home", "Pomodoro Timer"))
        self.StartStop.setText(_translate("Home", "Start Tracking"))

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
        

    def sendWorkNotif(self):
         notification.notify(
                    title = 'Pomodoro',
                    message = "Looks like You've been working hard. Time for a break",
                    app_icon = None,
                    timeout = 10,
                    toast = False
                )
    def update_restProgress(self):
        #condition is satisified only once until reset, i.e when this function is first called
        if self.min10actual == self.min10total: 
            self.sendWorkNotif()
        self.min10actual -= 1
        self.min10.setValue(self.min10actual)
        if self.min10actual <= 0:
            self.reset_timer()
            break_over = notification.notify(
                title = 'Pomodoro',
                message = 'Feeling productive?. Time to start another session.',
                app_icon = None,
                timeout = 10,
                toast = False
            )
        self.min10label.setText(self.update_min10_time())

    def reset_timer(self):
        self.timer.stop()
        self.min50actual = self.min50total
        self.min50.setValue(self.min50actual)
        self.min10actual = self.min10total
        self.min10.setValue(self.min10actual)
        self.Pause.setChecked(False)
        self.min50label.setText(self.settingconf.value("min50label","50m00s"))
        self.min10label.setText(self.settingconf.value("min10label","10m00s"))
        

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
        # self.MainContent.window().hide()

    def closeWindow(self):
        flag = self.settingconf.value("TrayToggle",True,type=bool)
        if flag == True:
            self.MainContent.window().hide()
        else:
            self.MainContent.window().close()

    

    def OpenSettings(self):
        self.settings_dialog = QDialog(self.Home)
        self.settings_dialog.setFixedSize(600, 481)
        self.settings_dialog.setWindowTitle('Settings')
        self.settings_dialog.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.settings_dialog.setModal(True)
        self.settings_dialog.setAttribute(Qt.WA_TranslucentBackground, True)
        
        self.title_bar = QFrame(self.settings_dialog)
        self.title_bar.setGeometry(0,0,600,36)
        self.title_bar.setObjectName("STitleBar")
        self.title_bar.setStyleSheet("QFrame{background-color: rgba(1, 1, 1, 1);border:1px solid #4C4C4C; border-top-left-radius: 20px; border-top-right-radius: 20px;}")
        
        self.close_button = QPushButton(self.title_bar)
        self.close_button.setGeometry(570, 7, 22, 22)
        self.close_button.setStyleSheet("QPushButton{background-color: rgb(48, 48, 48);border-radius:10px;icon-size:12px;}QPushButton:hover{background-color: rgb(255, 0, 0);border-radius:10px;icon:url(:/newPrefix/assets/close.png);}")
        self.close_button.clicked.connect(self.settings_dialog.close)
        self.close_button.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.STitleLabel = QLabel(self.settings_dialog)
        self.STitleLabel.setGeometry(220,0,159,36)
        bfont = QFont()
        bfont.setFamily("Poppins")
        bfont.setPointSize(10)
        bfont.setItalic(False)
        self.STitleLabel.setFont(bfont)
        hfont = QFont()
        hfont.setFamily("Poppins")
        hfont.setPointSize(10)
        hfont.setItalic(False)
        hfont.setBold(True)
        lfont = QFont()
        lfont.setFamily("Poppins Light")
        lfont.setPointSize(9)
        lfont.setItalic(True)
        self.STitleLabel.setFont(bfont)
        self.STitleLabel.setStyleSheet("QLabel{color:white;}")
        self.STitleLabel.setText("Settings")
        self.STitleLabel.setAlignment(Qt.AlignCenter)

        self.settingWindow = QFrame(self.settings_dialog)
        self.settingWindow.setGeometry(0,36,600,445)
        self.settingWindow.setStyleSheet("background-color:#1c1c1c;border-bottom-left-radius: 20px; border-bottom-right-radius: 20px;")
        screen_geometry = self.Home.screen().geometry()
        dialog_geometry = self.settings_dialog.geometry()
        x = (screen_geometry.width() - dialog_geometry.width()) // 2
        y = (screen_geometry.height() - dialog_geometry.height()) // 2
        self.settings_dialog.move(x, y)

        self.StartLabel = QLabel(self.settingWindow)
        self.StartLabel.setGeometry(32,23,222,47)
        self.StartLabel.setFont(hfont)
        self.StartLabel.setStyleSheet("QLabel{color:white;}")
        self.StartLabel.setText("Start with Windows")

        self.StartDesc = QLabel(self.settingWindow)
        self.StartDesc.setGeometry(32,52,469,47)
        self.StartDesc.setFont(bfont)
        self.StartDesc.setStyleSheet("QLabel{color:white;}")
        self.StartDesc.setText("Just Blink boots alongside windows to save you time")
        def changeWakeToggleState():
            self.settingconf.setValue("WakeToggle", self.WakeToggle.isChecked())
        self.WakeToggle = AnimatedToggle(checked_color="#86599D", pulse_checked_color="#CA69C6", parent=self.settingWindow)
        self.WakeToggleState = self.settingconf.value("WakeToggle",defaultValue=False,type=bool)
        self.WakeToggle.setChecked(self.WakeToggleState)
        self.WakeToggle.setGeometry(504, 50, 70, 50)
        self.WakeToggle.clicked.connect(changeWakeToggleState)

        
        self.DivisionLine = QFrame(self.settingWindow)
        self.DivisionLine.setGeometry(32,99,537,1)
        self.DivisionLine.setStyleSheet("background-color:#444444;")

        self.DivisionLine1 = QFrame(self.settingWindow)
        self.DivisionLine1.setGeometry(32,175,537,1)
        self.DivisionLine1.setStyleSheet("background-color:#444444;")

        self.DivisionLine2 = QFrame(self.settingWindow)
        self.DivisionLine2.setGeometry(32,250,537,1)
        self.DivisionLine2.setStyleSheet("background-color:#444444;")

        self.DivisionLine3 = QFrame(self.settingWindow)
        self.DivisionLine3.setGeometry(32,327,537,1)
        self.DivisionLine3.setStyleSheet("background-color:#444444;")

        self.TrayLabel = QLabel(self.settingWindow)
        self.TrayLabel.setGeometry(32,99,222,47)
        self.TrayLabel.setFont(hfont)
        self.TrayLabel.setStyleSheet("QLabel{color:white;}")
        self.TrayLabel.setText("Minimize to Tray")

        self.TrayDesc = QLabel(self.settingWindow)
        self.TrayDesc.setGeometry(32,139,469,24)
        self.TrayDesc.setFont(bfont)
        self.TrayDesc.setStyleSheet("QLabel{color:white;}")
        self.TrayDesc.setText("Just Blink stays in the tray after you close the app")

        def changeTrayToggleState():
            self.settingconf.setValue("TrayToggle", self.TrayToggle.isChecked())
        self.TrayToggle = AnimatedToggle(checked_color="#86599D", pulse_checked_color="#CA69C6", parent=self.settingWindow)
        self.TrayToggleState = self.settingconf.value("TrayToggle",defaultValue=False,type=bool)
        self.TrayToggle.setChecked(self.TrayToggleState)
        self.TrayToggle.setGeometry(504, 126, 70, 50)
        self.TrayToggle.clicked.connect(changeTrayToggleState)

        self.SensLabel = QLabel(self.settingWindow)
        self.SensLabel.setGeometry(32,175,222,40)
        self.SensLabel.setFont(hfont)
        self.SensLabel.setStyleSheet("QLabel{color:white;}")
        self.SensLabel.setText("Detection Sensitivity")

        self.SensDesc = QLabel(self.settingWindow)
        self.SensDesc.setGeometry(32,204,469,47)
        self.SensDesc.setFont(bfont)
        self.SensDesc.setStyleSheet("QLabel{color:white;}")
        self.SensDesc.setText("Change sensitivity of blink detection to suit you")

        self.SensSlider = QSlider(Qt.Horizontal, self.settingWindow)
        self.SensSlider.setGeometry(462, 212,107,30)
        self.SensSlider.setMinimum(85)
        self.SensSlider.setMaximum(95) 

        self.SensSlider.setTickPosition(QSlider.TicksBelow)
        self.SensSlider.setTickInterval(1)
        self.SensSlider.setSingleStep(1)
        self.SensSlider.setFixedWidth(107)
        self.SensSlider.setValue(self.settingconf.value('SensSliderValue',91))
        
        self.SensSlider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #2c2c2c;
                height: 2px;
                
            }QSlider::handle:horizontal {
                background: white;
                width: 14px;
                height: 14px;
                margin: -6px 0;
                border-radius: 7px;
            }QSlider::add-page:horizontal {
                background: #404040;
            }QSlider::sub-page:horizontal {
                background: #404040;
            }QSlider::tick:horizontal {
                background: #fff;
                height: 2px;
                width: 1px;
            }
        """)


        def changeSensVal(value):
            Sensi = value/100

            self.settingconf.setValue("SensValue",Sensi)
            self.settingconf.setValue("SensSliderValue",value)

            self.SensSlider.setValue(self.settingconf.value('SensSliderValue'))
        self.SensSlider.valueChanged.connect(changeSensVal)

        

        self.IntLabel = QLabel(self.settingWindow)
        self.IntLabel.setGeometry(32,251,222,47)
        self.IntLabel.setFont(hfont)
        self.IntLabel.setStyleSheet("QLabel{color:white;}")
        self.IntLabel.setText("Notification Interval")

        self.IntDesc = QLabel(self.settingWindow)
        self.IntDesc.setGeometry(32,280,434,47)
        self.IntDesc.setFont(bfont)
        self.IntDesc.setStyleSheet("QLabel{color:white;}")
        self.IntDesc.setText("Minimum interval between notifications")

        self.IntValue = QPushButton(self.settingWindow)
        self.IntValue.setGeometry(462, 288,107,30)
        self.IntValue.setStyleSheet("QPushButton{background-color:#2C2C2C;color:white;border-radius:15px;font-size:16px;font-family:\"Poppins\"}")
        self.IntValue.setText(self.settingconf.value("IntValue", "3 Mins"))
        def changeIntVal():
            if self.IntValue.text()=="3 Mins":
                self.IntValue.setText("5 Mins")
                self.settingconf.setValue('noti_int',300)
            elif self.IntValue.text()=="5 Mins":
                self.IntValue.setText("10 Mins")
                self.settingconf.setValue('noti_int',600)
            elif self.IntValue.text()=="10 Mins":
                self.IntValue.setText("15 Mins")
                self.settingconf.setValue('noti_int',900)
            else:
                self.IntValue.setText("3 Mins")
                self.settingconf.setValue('noti_int',180)
            self.settingconf.setValue("IntValue",self.IntValue.text())
        self.IntValue.clicked.connect(changeIntVal)


        self.PomLabel = QLabel(self.settingWindow)
        self.PomLabel.setGeometry(32,327,222,47)
        self.PomLabel.setFont(hfont)
        self.PomLabel.setStyleSheet("QLabel{color:white;}")
        self.PomLabel.setText("Pomodoro Duration")

        self.PomDesc = QLabel(self.settingWindow)
        self.PomDesc.setGeometry(32,356,434,47)
        self.PomDesc.setFont(bfont)
        self.PomDesc.setStyleSheet("QLabel{color:white;}")
        self.PomDesc.setText("Change the timer duration of Pomodoro Timer")

        self.PomValue = QPushButton(self.settingWindow)
        self.PomValue.setGeometry(462, 364,107,30)
        self.PomValue.setStyleSheet("QPushButton{background-color:#2C2C2C;color:white;border-radius:15px;font-size:16px;font-family:\"Poppins\"}")
        self.PomValue.setText(self.settingconf.value("PomValue", "60 Mins"))

        def changePomVal():

            if self.PomValue.text() == "60 Mins":
                self.PomValue.setText("30 Mins")
                self.min50total = 1500
                self.min10total = 300
                self.settingconf.setValue("min50label","25m00s")
                self.settingconf.setValue("min10label","05m00s")

            else:
                self.PomValue.setText("60 Mins")
                self.min50total = 3000
                self.min10total = 600
                self.settingconf.setValue("min50label","50m00s")
                self.settingconf.setValue("min10label","10m00s")
            self.min50.setRange(0, self.min50total)
            self.min10.setRange(0, self.min10total)
            self.reset_timer()

            self.settingconf.setValue("PomValue",self.PomValue.text())
            self.settingconf.setValue("min50total",self.min50total)
            self.settingconf.setValue("min10total",self.min10total)

        self.PomValue.clicked.connect(changePomVal)

        self.DivisionLine.raise_()
        self.DivisionLine1.raise_()
        self.DivisionLine2.raise_()
        self.DivisionLine3.raise_()
        self.WakeToggle.raise_()

        self.EndText = QLabel(self.settingWindow)
        self.EndText.setGeometry(185,410,229,24)
        self.EndText.setFont(lfont)
        self.EndText.setStyleSheet("QLabel {color:white;}")
        self.EndText.setOpenExternalLinks(True)
        self.EndText.setTextFormat(Qt.RichText)
        self.EndText.setText('Built using <a href="https://www.qt.io" style = "text-decoration:underline;color:white;">Qt</a>. Icons by <a href="https://icons8.com" style = "text-decoration:underline;color:white;">Icons8</a>')

        self.settings_dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())