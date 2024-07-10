from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from qfluentwidgets import SwitchButton

class CustomSwitchButton(SwitchButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Customize the switch button here
        self.setFixedSize(60, 30)  # Example size
        self.setStyleSheet("""
            SwitchButton::checked {
                background-color: #4CAF50;  # Green background when checked
            }
            SwitchButton::unchecked {
                background-color: #F44336;  # Red background when unchecked
            }
            SwitchButton::indicator::checked {
                background-color: #FFFFFF;  # White indicator when checked
            }
            SwitchButton::indicator::unchecked {
                background-color: #FFFFFF;  # White indicator when unchecked
            }
        """)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout(window)

    switch = CustomSwitchButton()
    layout.addWidget(switch)

    window.setLayout(layout)
    window.show()
    sys.exit(app.exec_())
