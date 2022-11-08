from functools import partial
import sys

from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QFrame,
    QMainWindow,
    QWidget,
    QPushButton,
)

class SideBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        print(self.parent().height())
