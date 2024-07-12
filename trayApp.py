import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon

class TrayApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        
        # Set up the icon
        self.appIcon = QIcon("assets/logos/48x48.ico")
        self.trayIco = QSystemTrayIcon()
        self.trayIco.setIcon(self.appIcon)
        self.trayIco.setVisible(True)
        
        # Set up the menu
        self.trayMenu = QMenu()
        self.add_menu_items()
        
        # Set context menu
        self.trayIco.setContextMenu(self.trayMenu)
        
        # Execute the app
        sys.exit(self.app.exec_())

    def add_menu_items(self):
        op1 = QAction("Show/Hide")
        op1.triggered.connect(self.show_hide)
        self.trayMenu.addAction(op1)
        
        op2 = QAction("Start Tracking")
        op2.triggered.connect(self.start_tracking)
        self.trayMenu.addAction(op2)
        
        op3 = QAction("Stop Tracking")
        op3.triggered.connect(self.stop_tracking)
        self.trayMenu.addAction(op3)
        
        op4 = QAction("Quit")
        op4.triggered.connect(self.quit)
        self.trayMenu.addAction(op4)

    def show_hide(self):
        print("Show/Hide clicked")

    def start_tracking(self):
        print("Start Tracking clicked")

    def stop_tracking(self):
        print("Stop Tracking clicked")

    def quit(self):
        print("Quit clicked")
        self.app.quit()

if __name__ == '__main__':
    TrayApp()
