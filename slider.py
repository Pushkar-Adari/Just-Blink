import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar, QWidget, QVBoxLayout
from PyQt5.QtGui import QBitmap, QPainter
from PyQt5.QtCore import Qt, QRect

def main():
    app = QApplication(sys.argv)

    # Create main window
    mainWindow = QMainWindow()
    mainWindow.setFixedSize(800, 600)
    mainWindow.setStyleSheet("""
        QMainWindow{
                             background-color:#1B1B1B;
        }
    """)
    # Create central widget and layout
    centralWidget = QWidget(mainWindow)
    layout = QVBoxLayout(centralWidget)

    # Create progress bar
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
    # Create bitmap for mask
    bm = QBitmap(progressBar.size())
    bm.fill(Qt.color0)
    p = QPainter(bm)
    p.setRenderHint(QPainter.HighQualityAntialiasing)  # Enable anti-aliasing for smoother edges
    p.setPen(Qt.color1)  # White pen to draw visible part in mask
    p.setBrush(Qt.color1)  # White brush to fill the rounded rectangle
    radius = 21  # Radius of the rounded corners
    p.drawRoundedRect(QRect(0, 0, bm.width(), bm.height()), radius, radius)
    p.end()

    progressBar.setMask(bm)

    # Add progress bar to layout and center it
    layout.addStretch()
    layout.addWidget(progressBar, 0, Qt.AlignCenter)
    layout.addStretch()

    centralWidget.setLayout(layout)
    mainWindow.setCentralWidget(centralWidget)

    # Show the main window
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
