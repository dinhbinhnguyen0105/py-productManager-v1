from functools import partial
import sys

from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QFrame,
    QTabBar,
    QMainWindow,
    QWidget,
    QPushButton,
)

class App(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setupUI()
    
    def _setupUI(self):
        self.centralWidget = QWidget()
        self.centralLayout = QVBoxLayout()

        self.btn1 = QPushButton('btn-1')
        self.btn2 = QPushButton('btn-2')
        self.btn3 = QPushButton('btn-3')
        self.btn1.clicked.connect(partial(self._onBtn1Clicked))
        self.btn2.clicked.connect(partial(self._onBtn2Clicked))
        self.btn3.clicked.connect(partial(self._onBtn3Clicked))

        self.widget1 = QFrame()
        self.widget1.setBaseSize(100, 100)
        self.widget1.setStyleSheet('background-color: blue')
        self.widget2 = QFrame()
        self.widget2.setBaseSize(100, 100)
        self.widget2.setStyleSheet('background-color: black')


        self.centralLayout.addWidget(self.btn1)
        self.centralLayout.addWidget(self.btn2)
        self.centralLayout.addWidget(self.btn3)
        self.centralWidget.setLayout(self.centralLayout)
        self.setCentralWidget(self.centralWidget)
        
        self.show()
    
    def _onBtn1Clicked(self):
        self.centralLayout.addWidget(self.widget1)
        
    def _onBtn2Clicked(self):
        self.centralLayout.addWidget(self.widget2)

    def _onBtn3Clicked(self):
        print(self.centralLayout.count())

        child = self.centralLayout.takeAt(0)
        del child


if __name__ == '__main__':
    app = QApplication([])
    window = App()
    sys.exit(app.exec())
    