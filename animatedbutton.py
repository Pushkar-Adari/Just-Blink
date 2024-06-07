import sys
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, pyqtProperty
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtGui import QColor

class BreathingButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCheckable(True)
        self.setFixedSize(267, 82)
        self.setStyleSheet("background-color: green;")

        self.clicked.connect(self.on_clicked)
        
        self.animation = QPropertyAnimation(self, b"breathingColor")
        self.animation.setDuration(1000)
        self.animation.setLoopCount(5)
        self.animation.setStartValue(QColor(192, 192, 192))  # Grey
        self.animation.setEndValue(QColor(255, 255, 255))    # White (for breathing effect)

        self._color = QColor(0, 255, 0)  # Initial color green
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.on_timeout)

    def on_clicked(self):
        self.setStyleSheet("background-color: grey;")
        self.animation.start()
        self.timer.start(5000)  # 5 seconds delay

    def on_timeout(self):
        self.setChecked(True)
        self.setStyleSheet("background-color: red;")

    def getBreathingColor(self):
        return self._color

    def setBreathingColor(self, color):
        self._color = color
        r, g, b, a = color.red(), color.green(), color.blue(), color.alpha()
        self.setStyleSheet(f"background-color: rgba({r}, {g}, {b}, {a});")

    breathingColor = pyqtProperty(QColor, getBreathingColor, setBreathingColor)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.button = BreathingButton("Click Me")

        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.setWindowTitle("Breathing Button Example")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
