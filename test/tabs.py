import sys

from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QFrame,
    QTabBar,
    QMainWindow,
)

class App(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle('tabs')
        self.setBaseSize(400, 400)
        self.createApp()
    
    def createApp(self):
        self.centralWidget = QFrame()
        centralLayout = QVBoxLayout()

        self.tabs = QTabBar()
        self.tabs.addTab('Tab 1')
        self.tabs.addTab('Tab 2')
        self.tabs.setTabsClosable(True)

        centralLayout.addWidget(self.tabs)

        self.tabs.tabCloseRequested.connect(self.close)


        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(centralLayout)

        self.show()
    
    def close(self, i):
        self.tabs.removeTab(i)

if __name__ == '__main__':
    app = QApplication([])
    window = App()
    sys.exit(app.exec())
    