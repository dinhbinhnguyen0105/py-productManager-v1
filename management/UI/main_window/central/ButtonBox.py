from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
)

from ....helper import _getExactlyPath

URL_STYLES = '\\py-production-management\\management\\UI\\main_window\\central\\styles.qss'

class ButtonBox(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        layout = QHBoxLayout()

        self.btnNext = QPushButton('Next')
        self.btnNext.setObjectName('btnNext')
        self.btnPrev = QPushButton('Prev')
        self.btnPrev.setObjectName('btnPrev')

        layout.addWidget(self.btnPrev)
        layout.addWidget(self.btnNext)
        
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)
        self.__setStyle()
    
    def __setStyle(self):
        with open(_getExactlyPath(URL_STYLES), 'r') as f:
            style = f.read()
        
        self.setStyleSheet(style)
