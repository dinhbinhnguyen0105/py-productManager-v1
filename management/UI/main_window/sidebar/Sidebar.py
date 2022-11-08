from PyQt6.QtWidgets import (
    QVBoxLayout,
    QFrame,
    QMainWindow,
    QPushButton,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from ....helper import _getExactlyPath

URL_ICON_PLUS = 'py-production-management\\assets\\icons\\plus.svg'
URL_STYLES = 'management\\UI\\main_window\\sidebar\\styles.qss'


class SideBar(QFrame):
    def __init__(self, parent=QMainWindow):
        super().__init__(parent)
        self.setFixedSize(int(self.parent().width() * 0.2), self.parent().height())
        self.layout = QVBoxLayout()

        iconUrl = _getExactlyPath(URL_ICON_PLUS)
        self.btnCreateNewListing = QPushButton('Create new listing')
        self.btnCreateNewListing.setIcon(QIcon(iconUrl))
        self.btnCreateNewListing.setObjectName('btnCreateNewListing')

        self.layout.addWidget(self.btnCreateNewListing)
        self.setLayout(self.layout)

        self._setStyles()       
    
    def _setStyles(self):
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setAlignment(self.btnCreateNewListing, Qt.AlignmentFlag.AlignTop)

        with open(URL_STYLES, 'r') as f:
            style = f.read()
        self.setStyleSheet(style)
        pass