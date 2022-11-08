import os
import json
import subprocess
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QFrame,
    QPushButton,
    QHBoxLayout,
    QWidget,
    QGridLayout,
    QLabel,
    QGridLayout,
    QPlainTextEdit
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from ....helper import _getExactlyPath
from ....helper import _randomIcon

PATH_CURRENT_PRODUCT = '\\py-production-management\\bin\\currentProduct.json'
PATH_STYLE = '\\py-production-management\\management\\UI\\dialog_create\\style.qss'
PATH_WARNING_ICON = '\\py-production-management\\assets\\icons\\warning.svg'
PATH_INFO_TEMPLATE = '\\py-production-management\\assets\\info_template.json'

class ImageCard(QWidget):
    def __init__(self, url, parent = None):
        super().__init__(parent)
        layout = QVBoxLayout()
        label = QLabel()
        label.setObjectName('imagecard')
        pixmap = QPixmap(url)
        pixmap = pixmap.scaled(120, 120)
        label.setPixmap(pixmap)
        layout.addWidget(label)
        self.setLayout(layout)
        self._setStyle()
    
    def _setStyle(self):
        self.setFixedSize(120, 120)

class ImageList(QWidget):
    def __init__(self, urls, parent = None):
        super().__init__(parent)
        layout = QGridLayout()
        displayImages = []

        if len(urls) > 8:
            for i in range(8):
                displayImages.append(urls[i])
        else:
            displayImages = urls

        rows = int(len(displayImages)/4)
        if int(len(displayImages)%4) > 0:
            rows += 1
        urlsReduce = len(displayImages)
        urlsIndex = 0
        for row in range(0, rows):
            for col in range(0, 4):
                layout.addWidget(ImageCard(displayImages[urlsIndex]), row, col, 1, 1)
                urlsReduce -= 1
                urlsIndex += 1
                if urlsReduce <= 0:
                    break
        self.setLayout(layout)

class DefaultInfo(QFrame):
    def __init__(self, payload, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        self.detailInfo = QPlainTextEdit()

        self.detailInfo.setPlainText(self._loadDefaultInfo(payload))
        layout.addWidget(self.detailInfo)
        self.setLayout(layout)
    
    def _loadDefaultInfo(self, payload):
        pathInfoTemplate = _getExactlyPath(PATH_INFO_TEMPLATE)
        if os.path.exists(pathInfoTemplate):
            with open(pathInfoTemplate, 'r', encoding='utf8') as f:
                infoTemplate = json.load(f)
            
            if payload['Category'] == 'Đất': 
                defaultInfo = infoTemplate['default_info_dat']
            defaultInfo = infoTemplate['default_info']
            icons = infoTemplate['icons']
            contact = infoTemplate['contact']
            
            defaultInfo = defaultInfo.replace('{icon}', _randomIcon(icons))
            defaultInfo = defaultInfo.replace('{category}', payload['Category'])
            defaultInfo = defaultInfo.replace('{price}', str(payload['Price']))
            defaultInfo = defaultInfo.replace('{ward}', payload['Ward'])
            defaultInfo = defaultInfo.replace('{district}', payload['District'])
            defaultInfo = defaultInfo.replace('{contact}', contact)
            defaultInfo = defaultInfo.replace('{street_name}', payload['Street name'])
            defaultInfo = defaultInfo.replace('{acreage}', str(payload['Acreage']))
            defaultInfo = defaultInfo.replace('{construction}', payload['Construction'])
            defaultInfo = defaultInfo.replace('{function}', payload['Function'])
            defaultInfo = defaultInfo.replace('{fuiture}', payload['Fuiture'])
            defaultInfo = defaultInfo.replace('{building_line}', payload['Building line'])
            defaultInfo = defaultInfo.replace('{legal}', payload['Legal'])
            defaultInfo = defaultInfo.replace('{description}', payload['Description'])

        return defaultInfo

class ButtonBox(QWidget):
    def __init__(self, payload, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.payload = payload

        self.btnOpen = QPushButton('Open')
        self.btnOpen.setObjectName('btnOpen')
        self.btnOpen.clicked.connect(lambda : self._onBtnOpenClick())
        self.btnEdit = QPushButton('Edit')
        self.btnEdit.setObjectName('btnEdit')
        self.btnEdit.clicked.connect(lambda : self._onBtnEditClick())
        self.btnRemove = QPushButton('Remove')
        self.btnRemove.setObjectName('btnRemove')
        self.btnRemove.clicked.connect(lambda : self._onBtnRemoveClick())
        self.btnOpenImageFolder = QPushButton('Folder')
        self.btnOpenImageFolder.setObjectName('btnOpenImageFolder')
        self.btnOpenImageFolder.clicked.connect(lambda : self._onbtnOpenImageFolderClick())

        layout.addWidget(self.btnOpen) 
        layout.addWidget(self.btnEdit) 
        layout.addWidget(self.btnRemove)
        layout.addWidget(self.btnOpenImageFolder)

        self.setLayout(layout)

    def _onBtnOpenClick(self):

        pass
    def _onBtnEditClick(self):

        pass
    def _onBtnRemoveClick(self):

        pass
    def _onbtnOpenImageFolderClick(self):
        print(self.payload['Folder path'])
        subprocess.Popen(rf'explorer /select, {self.payload["Folder path"]}')
        pass

class DetailProduct(QFrame):
    def __init__(self, payload, parent=None):
        super().__init__(parent)
        width = self.parent().width()

        self.centralLayout = QHBoxLayout()
        self.imageList = ImageList(payload['Image path'], self)
        self.imageList.setFixedWidth(int(width * 0.4))
        self.info = DefaultInfo(payload)
        self.info.setFixedWidth(int(width * 0.4))
        self.buttonBox = ButtonBox(payload)
        self.buttonBox.setFixedWidth(int(width * 0.2))


        
        self.centralLayout.addWidget(self.imageList)
        self.centralLayout.addWidget(self.info)
        self.centralLayout.addWidget(self.buttonBox)
        self.setLayout(self.centralLayout)

        self.__setStyle()
    def __setStyle(self):
        with open(_getExactlyPath(PATH_STYLE), 'r') as f:
            style = f.read()
        self.setStyleSheet(style)