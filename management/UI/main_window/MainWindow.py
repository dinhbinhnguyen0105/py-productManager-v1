from functools import partial
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt

from .sidebar.Sidebar import SideBar
from .central.Central import Central
from ..dialog_create.CreateDialog import CreateDialog
from ...APIs.APIs import _get
from ...Google.Drive import Drive

SIZE_WIDTH = 1400
SIZE_HEIGHT = int(SIZE_WIDTH/1.618) + 100

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Product management')
        self.setFixedSize(SIZE_WIDTH, SIZE_HEIGHT)

        self.centralWidget = QWidget()
        self.centralLayout = QHBoxLayout()

        self.sidebar = SideBar(self)
        self.central = Central(self)
        self.createDialog = CreateDialog()

        self.centralLayout.addWidget(self.sidebar)
        self.centralLayout.addWidget(self.central)

        self.drive = Drive()
        # self.drive._downloadImage('1CYsRwEEftygG7UP4MaMgvGNrBU9bqD27')

        self.centralWidget.setLayout(self.centralLayout)
        self.setCentralWidget(self.centralWidget)
        self.logic()
        self.__setStyle()


    
    def __setStyle(self):
        self.centralLayout.setContentsMargins(0,0,0,0)
        self.centralLayout.setAlignment(self.sidebar, Qt.AlignmentFlag.AlignLeft)
        self.setStyleSheet('background-color: white;')

    def logic(self):
        self.sidebar.btnCreateNewListing.clicked.connect(lambda : self.createDialog.show())
