from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPlainTextEdit,
)
from ...helper import _getExactlyPath

URL_STYLES = '\\py-production-management\\management\\UI\\dialog_create\\style.qss'


class PlainText(QWidget):
    def __init__(self, label = '', key = '', prevValue = '', placeholder = '', parent = None):
        super().__init__(parent)
        self.key = key
        layout = QVBoxLayout()
        _label = QLabel(label)
        _label.setObjectName('_label')
        self.inputField = QPlainTextEdit()
        self._setValue()
        layout.addWidget(_label)
        layout.addWidget(self.inputField)
        self.__setStyle()
        self.setLayout(layout)
    
    def _getValue(self):
        return {
            self.key : self.inputField.toPlainText()
        }
    def _setValue(self):
        self.inputField.setPlainText('')
    
    def __setStyle(self):
        self.setFixedHeight(120)

        self.inputField.setFixedHeight(100)
        with open(_getExactlyPath(URL_STYLES), 'r') as f:
            style = f.read()
        self.setStyleSheet(style)