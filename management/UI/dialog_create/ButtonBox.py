from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
)

from ...helper import _getExactlyPath

URL_STYLES = '\\py-production-management\\management\\UI\\dialog_create\\style.qss'

class ButtonBox(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        layout = QHBoxLayout()

        self.btnSave = QPushButton('Save')
        self.btnSave.setObjectName('btnSave')
        self.btnQuit = QPushButton('Quit')
        self.btnQuit.setObjectName('btnQuit')

        self.btnQuit.clicked.connect(lambda : self._onClickQuit())

        layout.addWidget(self.btnQuit)
        layout.addWidget(self.btnSave)
        
        self.setLayout(layout)
        self.__setStyle()
    
    def __setStyle(self):
        with open(_getExactlyPath(URL_STYLES), 'r') as f:
            style = f.read()
        self.setStyleSheet(style)

    def _onClickQuit(self):
        self.parent().close()
