from functools import partial
import sys

from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QFrame,
    QTabBar,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QPushButton,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt


class App(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUI()
        self.logic()
    
    def setupUI(self):
        width = 1400
        height = int(width/1.618)

        self.setWindowTitle('window')
        self.setFixedSize(width, height)

        self.centralWidget = QWidget()
        self.centralLayout = QHBoxLayout()

        self.sidebar = SideBar(self)
        self.centralLayout.addWidget(self.sidebar)

        self.centralWidget.setLayout(self.centralLayout)
        self.setCentralWidget(self.centralWidget)

        self.__setStyle()
        self.show()
    
    def logic(self):
        btnCreate = self.sidebar.btnCreateNewListing
        btnCreate.clicked.connect(self.onClick)
        pass

    def onClick(self):
        self.centralLayout.addWidget(QPushButton('bla'))
    
    def __setStyle(self):
        self.centralLayout.setSpacing(0)
        self.centralLayout.setContentsMargins(0,0,0,0)
        self.centralLayout.setAlignment(self.sidebar, Qt.AlignmentFlag.AlignLeft)
        
        pass

class SideBar(QFrame):
    def __init__(self, parent=QMainWindow):
        super().__init__(parent)

        self.setupUI()

    
    def setupUI(self):
        self.setFixedSize(int(self.parent().width()*0.25), self.parent().height())
        layout = QVBoxLayout()

        self.btnCreateNewListing = QPushButton('Create new listing')
        self.btnCreateNewListing.setIcon(QIcon('test\\plus-solid.svg'))
        self.btnCreateNewListing.setStyleSheet('''
            QPushButton {
                height: 36px;
                margin: 12px;
                border: None;
                border-radius: 6px;
                color: rgb(24, 119, 242);
                background-color: rgb(231, 243, 255);
                font-weight: bold;
            }
        ''')

        layout.addWidget(self.btnCreateNewListing)

        self.setLayout(layout)

        layout.setAlignment(self.btnCreateNewListing, Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0,0,0,0)
        self.setStyleSheet('border: 1px solid black;')
        pass


def main():
    app = QApplication([])
    window = App()
    window.setStyleSheet('''
        QMainWindow {
            background-color: white;
        }
    ''')

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
    