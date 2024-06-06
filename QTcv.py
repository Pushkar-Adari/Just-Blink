import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, QElapsedTimer
import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector

class BlinkDetectorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Blink Detector")
        self.setGeometry(100, 100, 400, 200)
        
        # Initialize UI elements
        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_detection)
        
        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_detection)
        
        self.blink_label = QLabel("Blinks: 0", self)
        self.avg_label = QLabel("Average Blinks/Min: 0", self)
        
        layout = QVBoxLayout()
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.blink_label)
        layout.addWidget(self.avg_label)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        # Initialize OpenCV
        self.cap = cv2.VideoCapture(0)
        self.detector = FaceMeshDetector(maxFaces=1)
        self.idlist = [22, 23, 24, 26, 110, 130, 157, 158, 159, 160, 161, 243]
        self.ratioList = []
        self.blinkCount = 0
        self.counter = 0
        
        # Timer for updating frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # Elapsed timer
        self.elapsed_timer = QElapsedTimer()
        
    def start_detection(self):
        self.blinkCount = 0
        self.counter = 0
        self.ratioList = []
        self.elapsed_timer.start()
        self.timer.start(30)  # Update frame every 30 ms
        
    def stop_detection(self):
        self.timer.stop()
        
    def update_frame(self):
        success, img = self.cap.read()
        if not success:
            return
        
        img, faces = self.detector.findFaceMesh(img, draw=False)
        if faces:
            face = faces[0]
            eyeTop = face[159]
            eyeBot = face[23]
            eyeLeft = face[130]
            eyeRight = face[243]
            eyeLength, _ = self.detector.findDistance(eyeTop, eyeBot)
            eyeWidth, _ = self.detector.findDistance(eyeLeft, eyeRight)
            ratio = (eyeLength / eyeWidth) * 100
            self.ratioList.append(ratio)
            if len(self.ratioList) > 7:
                self.ratioList.pop(0)
            avgRatio = sum(self.ratioList) / len(self.ratioList)
            dynamic_limit = avgRatio * 0.9
            if ratio < dynamic_limit and self.counter == 0:
                self.blinkCount += 1
                self.counter = 1
            if self.counter != 0:
                self.counter += 1
                if self.counter > 10:
                    self.counter = 0
            
            # Update blink label
            self.blink_label.setText(f"Blinks: {self.blinkCount}")
            
            # Calculate and update average blinks per minute
            elapsed_time_sec = self.elapsed_timer.elapsed() / 1000  # Convert to seconds
            elapsed_time_min = elapsed_time_sec / 60  # Convert to minutes
            if elapsed_time_min > 0:
                avg_blinks_per_min = self.blinkCount / elapsed_time_min
                self.avg_label.setText(f"Average Blinks/Min: {avg_blinks_per_min:.2f}")
        
    def closeEvent(self, event):
        self.cap.release()
        cv2.destroyAllWindows()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BlinkDetectorApp()
    window.show()
    sys.exit(app.exec_())
