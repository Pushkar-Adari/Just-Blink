import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QProgressBar, QPushButton, QLabel
from PyQt5.QtGui import QBitmap, QPainter
from PyQt5.QtCore import QTimer, Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.total_time = 30  # total countdown time in seconds
        self.remaining_time = self.total_time

        self.setFixedSize(800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1B1B1B;
            }
        """)

        self.centralWidget = QWidget(self)
        self.layout = QVBoxLayout(self.centralWidget)
        
        self.progressBar = QProgressBar()
        self.progressBar.setFixedSize(530, 43)
        self.progressBar.setRange(0, self.total_time)  # Set the range of the progress bar from 0 to 3000
        self.progressBar.setValue(self.total_time)  # Initial value for the progress bar

        self.progressBar.setStyleSheet("""
            QProgressBar {
                border-radius: 21px;
                text-align: center;
                color:transparent;
            }
            QProgressBar::chunk {
                background-color: #05B8CC;
                border-radius: 21px;
            }
        """)

        self.btn = QPushButton("Start", self)
        self.btn.setCheckable(True)

        self.btn.move(350, 200)
        self.btn.toggled.connect(self.toggle_timer)

        self.resetBtn = QPushButton("Reset", self)
        self.resetBtn.move(500,200)
        self.resetBtn.clicked.connect(self.reset_timer)

        self.timer = QTimer()
        self.timer.setInterval(1000)  # 1000 ms = 1 second
        self.timer.timeout.connect(self.update_progress)

        # Creating a bitmap mask for rounded corners
        bm = QBitmap(self.progressBar.size())
        bm.fill(Qt.white)
        p = QPainter(bm)
        p.setRenderHint(QPainter.HighQualityAntialiasing)
        p.setPen(Qt.black)
        p.setBrush(Qt.black)
        radius = 21
        p.drawRoundedRect(self.progressBar.rect(), radius, radius)
        p.end()
        self.progressBar.setMask(bm)

        # Adding the label for "TIMER"
        self.timer_label = QLabel("TIMER", self.centralWidget)
        self.timer_label.setStyleSheet("color: white;")
        self.timer_label.setGeometry(QtCore.QRect(60, 280, 530, 43))
        self.timer_label.setAlignment(Qt.AlignCenter)

        self.layout.addStretch()
        self.layout.addWidget(self.progressBar, 0, Qt.AlignCenter)
        self.layout.addStretch()
        self.timer_label.raise_()
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)

    def toggle_timer(self, checked):
        if checked:
            self.btn.setText("Stop")
            self.timer.start()
        else:
            self.btn.setText("Start")
            self.timer.stop()

    def update_progress(self):
        self.remaining_time -= 1
        self.progressBar.setValue(self.remaining_time)

    def reset_timer(self):
        self.timer.stop()
        self.remaining_time = self.total_time
        self.progressBar.setValue(self.total_time)


def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
