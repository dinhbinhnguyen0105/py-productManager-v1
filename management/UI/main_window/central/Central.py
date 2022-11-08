import json
import os
from functools import partial
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QFrame,
    QMainWindow,
    QPushButton,
    QHBoxLayout,
    QWidget,
    QGridLayout,
    QTabWidget
)
from PyQt6.QtCore import Qt, QObject, QThread, pyqtSignal

from .ListProduct import ListProduct
from .DetailProduct import DetailProduct
from ....helper import _getExactlyPath

PATH_CURRENT_PRODUCT = '\\py-production-management\\bin\\currentProduct.json'


class Central(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setFixedSize(int(self.parent().width()*0.8), self.parent().height())
        self.centralLayout = QVBoxLayout()
        self.listProduct = ListProduct(self)
        self.listProduct.setFixedSize(int(self.parent().width()), int(self.parent().height()*0.5))

        self.detailProduct = QWidget()     

        self.listProduct.currentProductChanged.connect(self.displayCurrentProduct)

        self.centralLayout.addWidget(self.listProduct)
        self.setLayout(self.centralLayout)

    def displayCurrentProduct(self, e):
        if self.detailProduct:
            self.centralLayout.removeWidget(self.detailProduct)
            self.detailProduct.deleteLater()
        self.detailProduct  = DetailProduct(e, self)

        self.centralLayout.addWidget(self.detailProduct)