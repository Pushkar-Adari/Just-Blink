import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar, QWidget, QVBoxLayout
from PyQt5.QtGui import QBitmap, QPainter
from PyQt5.QtCore import Qt, QRect

def main():
    app = QApplication(sys.argv)

    mainWindow = QMainWindow()
    mainWindow.setFixedSize(800, 600)
    mainWindow.setStyleSheet("""
        QMainWindow{
                             background-color:#1B1B1B;
        }
    """)
    centralWidget = QWidget(mainWindow)
    layout = QVBoxLayout(centralWidget)

    progressBar = QProgressBar()
    progressBar.setFixedSize(106, 43)
    progressBar.setStyleSheet("""
        QProgressBar {
            border-radius: 21px;
            text-align: center;
        }
        QProgressBar::chunk {
            background-color: #05B8CC;
            border-radius: 21px;

        }
    """)
    progressBar.setValue(0)
    bm = QBitmap(progressBar.size())
    bm.fill(Qt.color0)
    p = QPainter(bm)
    p.setRenderHint(QPainter.HighQualityAntialiasing)  
    p.setPen(Qt.color1)  
    p.setBrush(Qt.color1)  
    radius = 21  
    p.drawRoundedRect(QRect(0, 0, bm.width(), bm.height()), radius, radius)
    p.end()

    progressBar.setMask(bm)

    
    layout.addStretch()
    layout.addWidget(progressBar, 0, Qt.AlignCenter)
    layout.addStretch()

    centralWidget.setLayout(layout)
    mainWindow.setCentralWidget(centralWidget)

    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
