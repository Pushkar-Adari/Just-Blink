import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout

class HoverButton(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.button = QPushButton('Hover Me')
        self.label = QLabel('')
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.button.enterEvent = self.on_enter
        self.button.leaveEvent = self.on_leave

    def on_enter(self, event):
        self.label.setText('<div style="padding: 10px; text-align: justify;">This is a button</div>')

    def on_leave(self, event):
        self.label.setText('')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HoverButton()
    window.setWindowTitle('Hover Button')
    window.setGeometry(100, 100, 300, 150)
    window.show()
    sys.exit(app.exec_())
