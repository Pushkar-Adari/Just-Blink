import sys
from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout

class CustomWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(100, 100, 400, 300)

        self.dragPos = QPoint()

        # Custom title bar
        self.titleBar = QWidget(self)
        self.titleBar.setFixedHeight(30)
        self.titleBar.setStyleSheet("background-color: #444444; color: white;")

        self.titleLabel = QLabel("Custom Title Bar", self.titleBar)
        self.titleLabel.setStyleSheet("margin-left: 10px;")

        self.closeButton = QPushButton('X', self.titleBar)
        self.closeButton.setStyleSheet("background-color: red; border: none; color: white;")
        self.closeButton.setFixedSize(30, 30)
        self.closeButton.clicked.connect(self.close)

        titleLayout = QHBoxLayout(self.titleBar)
        titleLayout.addWidget(self.titleLabel)
        titleLayout.addStretch()
        titleLayout.addWidget(self.closeButton)
        titleLayout.setContentsMargins(0, 0, 0, 0)
        self.titleBar.setLayout(titleLayout)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.titleBar)
        self.mainLayout.addStretch()
        self.setLayout(self.mainLayout)

        # Connect mouse events for dragging
        self.titleBar.mousePressEvent = self.mousePressEvent
        self.titleBar.mouseMoveEvent = self.mouseMoveEvent

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)
            event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = CustomWindow()
    mainWin.show()
    sys.exit(app.exec_())
