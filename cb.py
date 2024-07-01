import sys
from PyQt5 import QtWidgets
from qtwidgets import AnimatedToggle

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Centered Toggle Switch")
        self.setGeometry(100, 100, 600, 400)  # Set window position and size
        
        toggle = AnimatedToggle(checked_color="#FFB000", pulse_checked_color="rgba(0,0,0,0)")  # Animated toggle with custom colors
        toggle.setGeometry(290, 180, 30, 40)  # Set toggle switch position relative to window
        
        self.setCentralWidget(toggle)

app = QtWidgets.QApplication([])
w = Window()
w.show()
sys.exit(app.exec_())
