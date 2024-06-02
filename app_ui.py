from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QBitmap, QPainter, QIcon
from PyQt5.QtCore import Qt, QRect, QTimer

class Ui_Home(object):
    def setupUi(self, Home):
        #///////// VALUES ///////
        self.min50total = 3000
        self.min10total = 600
        self.min10actual = self.min10total
        self.min50actual = self.min50total

        #///////// HOME /////////

        Home.setObjectName("Home")
        Home.setFixedSize(800, 570)
        Home.setAutoFillBackground(False)
        Home.setStyleSheet("")
        self.Central = QtWidgets.QWidget(Home)
        self.Central.setStyleSheet("")
        self.Central.setObjectName("Central")

        #///////// START/STOP  /////////

        self.StartStop = QtWidgets.QPushButton(self.Central)
        self.StartStop.setEnabled(True)
        self.StartStop.setGeometry(QtCore.QRect(502, 355, 267, 82))
        font = QtGui.QFont()
        font.setFamily("Poppins SemiBold")
        font.setPointSize(15)
        font.setItalic(False)
        self.StartStop.setFont(font)
        self.StartStop.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.StartStop.setStyleSheet("background-color: rgba(43, 11, 11,0.5);\n"
                                     "border-radius:20;\n"
                                     "color: rgb(249,35,35);\n"
                                     "font: 63 14.5pt \"Poppins SemiBold\";\n"
                                     "\n"
                                     "")
        self.StartStop.setCheckable(True)
        self.StartStop.setChecked(False)
        self.StartStop.setObjectName("StartStop")

        #///////// LOGO /////////

        self.Logo = QtWidgets.QLabel(self.Central)
        self.Logo.setGeometry(QtCore.QRect(50, 28, 207, 55))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(24)
        font.setBold(True)
        font.setItalic(False)
        self.Logo.setFont(font)
        self.Logo.setStyleSheet("color:white;\n"
                                "background-color: rgba(255, 255, 255, 0);\n"
                                "")
        self.Logo.setObjectName("Logo")

        #///////// PROFILE /////////

        self.Profile = QtWidgets.QToolButton(self.Central)
        self.Profile.setGeometry(QtCore.QRect(663, 33, 43, 43))
        self.Profile.setStyleSheet("background-color: rgb(19, 19, 19);\n"
                                   "border-radius:21px;\n"
                                   "icon-size:25px;")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/assets/user.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Profile.setIcon(icon)
        self.Profile.setObjectName("Profile")

        #///////// SETTINGS /////////

        self.Setting = QtWidgets.QToolButton(self.Central)
        self.Setting.setGeometry(QtCore.QRect(718, 33, 43, 43))
        self.Setting.setStyleSheet("background-color: rgb(19, 19, 19);\n"
                                   "border-radius:21px;\n"
                                   "icon-size:25px;")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/newPrefix/assets/setting.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Setting.setIcon(icon1)
        self.Setting.setObjectName("Setting")

        #///////// AVERAGE /////////

        self.Avg = QtWidgets.QFrame(self.Central)
        self.Avg.setGeometry(QtCore.QRect(502, 108, 267, 111))
        self.Avg.setStyleSheet("background-color: rgba(19, 19, 19,    0.7);\n"
                               "border-radius:20px;")
        self.Avg.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Avg.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Avg.setObjectName("Avg")
        self.label = QtWidgets.QLabel(self.Avg)
        self.label.setGeometry(QtCore.QRect(0, 0, 263, 61))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(14)
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
                                 "color:white;\n"
                                 "")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        #///////// WEEKLY /////////

        self.Week = QtWidgets.QFrame(self.Central)
        self.Week.setGeometry(QtCore.QRect(502, 230, 267, 111))
        self.Week.setStyleSheet("background-color: rgba(19, 19, 19,    0.7);\n"
                                "border-radius:20px;")
        self.Week.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Week.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Week.setObjectName("Week")
        self.label_2 = QtWidgets.QLabel(self.Week)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 263, 61))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(14)
        font.setItalic(True)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color: rgba(0,0,0,0);\n"
                                   "color:white;")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        #///////// GRAPH /////////

        self.Graph = QtWidgets.QFrame(self.Central)
        self.Graph.setGeometry(QtCore.QRect(31, 108, 458, 329))
        self.Graph.setStyleSheet("background-color: rgba(19, 19, 19,    0.7);\n"
                                 "border-radius:20px;")
        self.Graph.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Graph.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Graph.setObjectName("Graph")

        #///////// TIMER /////////

        self.TimerLabel = QtWidgets.QLabel(self.Central)
        self.TimerLabel.setGeometry(QtCore.QRect(43, 450, 210, 44))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        self.TimerLabel.setFont(font)
        self.TimerLabel.setStyleSheet("color:white;\n"
                                      "font-size: 14.5pt;\n"
                                      "background-color: rgba(0, 0, 0, 0);")
        self.TimerLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.TimerLabel.setFrameShadow(QtWidgets.QFrame.Plain)
        self.TimerLabel.setWordWrap(False)
        self.TimerLabel.setObjectName("TimerLabel")

        self.Pause = QtWidgets.QToolButton(self.Central)
        self.Pause.setGeometry(QtCore.QRect(678, 498, 43, 43))
        self.Pause.setStyleSheet("background-color: rgb(19, 19, 19);\n"
                                 "border-radius:21px;\n"
                                 "icon-size:20px;")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/newPrefix/assets/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(":/newPrefix/assets/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.Pause.setIcon(icon2)
        self.Pause.setCheckable(True)
        self.Pause.setChecked(False)
        self.Pause.setObjectName("Pause")
        self.Pause.toggled.connect(self.toggle_timer)

        self.Reset = QtWidgets.QToolButton(self.Central)
        self.Reset.setGeometry(QtCore.QRect(726, 498, 43, 43))
        self.Reset.setStyleSheet("background-color: rgb(19, 19, 19);\n"
                                 "border-radius:21px;\n"
                                 "icon-size:20px;")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/newPrefix/assets/reset.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Reset.setIcon(icon3)
        self.Reset.setObjectName("Reset")
        self.Reset.clicked.connect(self.reset_timer)

        self.Name = QtWidgets.QFrame(self.Central)
        self.Name.setGeometry(QtCore.QRect(586, 38, 119, 32))
        self.Name.setStyleSheet("background-color: rgba(19, 19, 19,    0.7);\n"
                                "border-radius:15px\n"
                                ";")
        self.Name.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Name.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Name.setObjectName("Name")

        self.Background = QtWidgets.QFrame(self.Central)
        self.Background.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.Background.setStyleSheet("border-image: url(:/newPrefix/b2.png) 0 0 0 0 stretch stretch;\n"
                                      "border-width: 0px;\n"
                                      "")
        self.Background.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Background.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Background.setObjectName("Background")

        #///////// PROGRESS BARS /////////

        self.min10 = QtWidgets.QProgressBar(self.Central)
        self.min10.setGeometry(QtCore.QRect(32, 498, 106, 43))
        self.min10.setStyleSheet("QProgressBar{\n"
                                 "background-color:rgba(45,45,45,0.5);\n"
                                 "border-radius:21px;\n"
                                 "text-align:center;\n"
                                 "color:transparent;\n"
                                 "}\n"
                                 "QProgressBar::chunk{\n"
                                 "background:qLineargradient(spread:pad, x1:0, y1:0, x2:1, x2:1, stop:0 rgba(52,30,63,255),stop:1 rgba(134,89,157,255));\n"
                                 "border-radius:21px;\n"
                                 "}")
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
        p.drawRoundedRect(QRect(0, 0, bm.width(), bm.height()), radius, radius)
        p.end()
        self.min10.setMask(bm)
        self.min10label = QtWidgets.QLabel(self.Central)
        self.min10label.setGeometry(QtCore.QRect(32, 498, 106, 43))
        font = QtGui.QFont()
        font.setFamily("Poppins ExtraLight")
        font.setPointSize(9)
        font.setItalic(False)
        self.min10label.setFont(font)
        self.min10label.setStyleSheet(
            "QLabel{\n"
            "color:white;\n"
            "}"
        )
        self.min10label.setText("10m00s")
        self.min10label.setAlignment(Qt.AlignCenter)
        self.min50 = QtWidgets.QProgressBar(self.Central)
        self.min50.setGeometry(QtCore.QRect(143, 498, 530, 43))
        self.min50.setStyleSheet("QProgressBar{\n"
                                 "background-color:rgba(45,45,45,0.5);\n"
                                 "border-radius:21px;\n"
                                 "text-align:center;\n"
                                 "color:transparent;\n"
                                 "}\n"
                                 "QProgressBar::chunk{\n"
                                 "background:qLineargradient(spread:pad, x1:0, y1:0, x2:1, x2:1, stop:0 rgba(50,51,113,255),stop:1 rgba(2,19,51,255));\n"
                                 "border-radius:21px;\n"
                                 "}")
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
        p.drawRoundedRect(QRect(0, 0, bm.width(), bm.height()), radius, radius)
        p.end()
        self.min50.setMask(bm)

        self.min50label = QtWidgets.QLabel(self.Central)
        self.min50label.setGeometry(QtCore.QRect(143, 498, 530, 43))
        font = QtGui.QFont()
        font.setFamily("Poppins ExtraLight")
        font.setPointSize(9)
        font.setItalic(False)
        self.min50label.setFont(font)
        self.min50label.setStyleSheet(
            "QLabel{\n"
            "color:white;\n"
            "}"
        )
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
        self.label.setText(_translate("Home", "Average Blinks:"))
        self.label_2.setText(_translate("Home", "Weekly Report :"))
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

    def update_restProgress(self):
        self.min10actual -= 1
        self.min10.setValue(self.min10actual)
        if self.min10actual <= 0:
            self.reset_timer()

    def reset_timer(self):
        self.timer.stop()
        self.min50actual = self.min50total
        self.min50.setValue(self.min50actual)
        self.min10actual = self.min10total
        self.min10.setValue(self.min10actual)
        self.Pause.setChecked(False)

import rc_rc
