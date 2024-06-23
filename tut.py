import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt, QTimer

CONFIG_FILE = "config.json"

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome")
        self.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout()
        self.label = QLabel("Welcome to the App!", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        
        self.setLayout(layout)
        QTimer.singleShot(3000, self.close)  # Close splash screen after 3 seconds

class Tutorial(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tutorial")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.label = QLabel("Please enter your name:", self)
        layout.addWidget(self.label)

        self.name_input = QLineEdit(self)
        layout.addWidget(self.name_input)

        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.submit_name)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit_name(self):
        name = self.name_input.text()
        if name:
            QMessageBox.information(self, "Welcome", f"Hello, {name}!")
            self.close()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter your name.")

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main App")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.label = QLabel("This is the main application.", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.setLayout(layout)

def check_first_time():
    if not os.path.exists(CONFIG_FILE):
        return True
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    return not config.get('tutorial_shown', False)

def mark_tutorial_shown():
    with open(CONFIG_FILE, 'w') as f:
        config = {'tutorial_shown': True}
        json.dump(config, f)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    if check_first_time():
        splash = SplashScreen()
        splash.show()
        splash.closeEvent = lambda event: (Tutorial().show(), mark_tutorial_shown())
    else:
        main_app = MainApp()
        main_app.show()

    sys.exit(app.exec_())
