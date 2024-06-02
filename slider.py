import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QProgressBar, QPushButton
from PyQt5.QtGui import QBitmap, QPainter
from PyQt5.QtCore import QTimer, Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.total_time = 120  # total countdown time in seconds
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
        self.btn.move(350, 200)
        self.btn.clicked.connect(self.start)

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

        self.layout.addStretch()
        self.layout.addWidget(self.progressBar, 0, Qt.AlignCenter)
        self.layout.addStretch()

        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)

    def start(self):
        self.timer.start()

    def update_progress(self):
        self.remaining_time -= 1
        self.progressBar.setValue(self.remaining_time)

        if self.remaining_time <= 0:
            self.timer.stop()

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
