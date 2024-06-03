import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QHBoxLayout

class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(30)
        self.setStyleSheet("background-color: #2E2E2E; color: white;")

        self.minimizeButton = QPushButton("-")
        self.closeButton = QPushButton("X")
        self.minimizeButton.setFixedSize(30, 30)
        self.closeButton.setFixedSize(30, 30)

        self.minimizeButton.setStyleSheet("background-color: #2E2E2E; color: white;")
        self.closeButton.setStyleSheet("background-color: #2E2E2E; color: white;")

        self.minimizeButton.clicked.connect(self.minimizeWindow)
        self.closeButton.clicked.connect(self.closeWindow)

        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.minimizeButton)
        layout.addWidget(self.closeButton)
        self.setLayout(layout)

    def minimizeWindow(self):
        self.window().showMinimized()

    def closeWindow(self):
        self.window().close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 600)
        
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.titleBar = CustomTitleBar(self)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.titleBar)
        mainLayout.addStretch()

        self.centralWidget.setLayout(mainLayout)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFFFFF;
            }
            QPushButton {
                border: none;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
