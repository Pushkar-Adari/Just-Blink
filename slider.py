import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider
from PyQt5.QtCore import Qt

class SliderWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create QSlider
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(10)  # 11 stops from 0 to 10
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.setSingleStep(1)
        self.slider.setFixedWidth(107)

        # Set the style
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #2c2c2c;
                height: 2px;
            }

            QSlider::handle:horizontal {
                background: white;
                width: 14px;
                height: 14px;
                margin: -6px 0;
                border-radius: 7px;
            }

            QSlider::add-page:horizontal {
                background: #2c2c2c;
            }

            QSlider::sub-page:horizontal {
                background: #2c2c2c;
            }

            QSlider::tick:horizontal {
                background: #2c2c2c;
                height: 2px;
                width: 1px;
            }
        """)

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SliderWindow()
    window.show()
    sys.exit(app.exec_())
