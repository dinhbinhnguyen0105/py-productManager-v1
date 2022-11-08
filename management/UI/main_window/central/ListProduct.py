import os
import json
from PyQt6.QtWidgets import (
    QFrame,
    QWidget,
    QLineEdit,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QTableView
)
from PyQt6.QtCore import QSortFilterProxyModel,  QObject, QThread, pyqtSignal
from PyQt6.QtGui import QMovie, QStandardItemModel, QStandardItem

from ....APIs.APIs import _get
from ....Google.Drive import Drive
from ....helper import _getExactlyPath

PATH_DATA = '\\py-production-management\\bin\\data.json'
PATH_CURRENT_PRODUCT = '\\py-production-management\\bin\\currentProduct.json'
PATH_FOLDER_OF_IMAGES = 'py-production-management\\bin\\images'
PATH_LOADING_ANIMATION = 'py-production-management\\assets\\animation\\loading.gif'
PATH_STYLE = '\\py-production-management\\management\\UI\\dialog_create\\style.qss'
PATH_EDIT_ICON = '\\py-production-management\\assets\\icons\\edit.svg'
PATH_REMOVE_ICON = '\\py-production-management\\assets\\icons\\remove.svg'
PATH_OPEN_ICON = '\\py-production-management\\assets\\icons\\open.svg'
FOLDER_KEY = 'Folder Id'
IMAGE_KEY = 'Image Id'

HEADER = ['ID', 'Category', 'Ward', 'Street name', 'Acreage',  'Price', 'Legal', 'Building line']


class Table(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)

class ListProduct(QFrame): 
    currentProductChanged = pyqtSignal(object)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.centralLayout = QVBoxLayout()
        self._handleLoadData()
        self.searchField = SearchField()
        self.searchField.setFixedWidth(int(self.parent().width() * 0.8))
        self.table = Table()

        self.model = QStandardItemModel()
        self.model.setColumnCount(len(HEADER))
        self.model.setHorizontalHeaderLabels(HEADER)
        self.filterProxyModel = SortFilterProxyModel()

        self.setLayout(self.centralLayout)

        with open(_getExactlyPath(PATH_STYLE), 'r') as f:
            style = f.read()
        self.setStyleSheet(style)

    def _handleLoadData(self):
        self.thread = QThread(self)
        self.loadData = LoadData()
        self.loadData.moveToThread(self.thread)

        self.thread.started.connect(self.loadData.run)
        self.thread.finished.connect(self.thread.deleteLater)

        self.loadData.getAPIsStatus.connect(self._reportAPIsStatus)
        self.loadData.progress.connect(self._reportProgress)
        self.loadData.finished.connect(self._reportFinished)
        self.loadData.finished.connect(self.loadData.deleteLater)
        self.loadData.finished.connect(self.thread.quit)

        self.thread.start()
    
    def _reportAPIsStatus(self, e):
        if e is False:
            self.loadingScreen = LoadingScreen(self)
            self.centralLayout.addWidget(self.loadingScreen)
        else:
            self.centralLayout.removeWidget(self.loadingScreen)
            self.loadingScreen.deleteLater()
            self.loadingScreen = None

            self.centralLayout.addWidget(self.searchField)
            self.centralLayout.addWidget(self.table)
# headers = ['ID', 'Category', 'Ward', 'Street name', 'Acreage',  'Price', 'Legal', 'Building line']

    def _reportProgress(self, e):
        _id = QStandardItem(str(e['ID']))
        _category = QStandardItem(str(e['Category']))
        _ward = QStandardItem(str(e['Ward']))
        _streetName = QStandardItem(str(e['Street name']))
        _acreage = QStandardItem(str(e['Acreage']))
        _price = QStandardItem(str(e['Price']))
        _legal = QStandardItem(str(e['Legal']))
        _buildingLine = QStandardItem(str(e['Building line']))

        rowPosition = self.model.rowCount()
        self.model.insertRow(rowPosition)

        self.model.setItem(rowPosition, 0, _id)
        self.model.setItem(rowPosition, 1, _category)
        self.model.setItem(rowPosition, 2, _ward)
        self.model.setItem(rowPosition, 3, _streetName)
        self.model.setItem(rowPosition, 4, _acreage)
        self.model.setItem(rowPosition, 5, _price)
        self.model.setItem(rowPosition, 6, _legal)
        self.model.setItem(rowPosition, 7, _buildingLine)

        self.filterProxyModel.setSourceModel(self.model)

        self.searchField.searchFieldId.textChanged.connect(lambda text, col=0: self.filterProxyModel.setFilterByColumn(text, col))
        self.searchField.searchFieldCategory.textChanged.connect(lambda text, col=1: self.filterProxyModel.setFilterByColumn(text, col))
        self.searchField.searchFieldWard.textChanged.connect(lambda text, col=2: self.filterProxyModel.setFilterByColumn(text, col))
        self.searchField.searchFieldStreetName.textChanged.connect(lambda text, col=3: self.filterProxyModel.setFilterByColumn(text, col))
        self.searchField.searchFieldAcreage.textChanged.connect(lambda text, col=4: self.filterProxyModel.setFilterByColumn(text, col))
        self.searchField.searchFieldPrice.textChanged.connect(lambda text, col=5: self.filterProxyModel.setFilterByColumn(text, col))
        self.searchField.searchFieldLegal.textChanged.connect(lambda text, col=6: self.filterProxyModel.setFilterByColumn(text, col))
        self.searchField.searchFieldBuildingLine.textChanged.connect(lambda text, col=7: self.filterProxyModel.setFilterByColumn(text, col))

        self.table.setModel(self.filterProxyModel)
         
    def _reportFinished(self, e):
        with open(_getExactlyPath(PATH_DATA), 'w', encoding='utf8') as f:
            json.dump(e, f)
        self.table.selectionModel().selectionChanged.connect(lambda : self.onChange(e))

    def onChange(self, payload):
        currentRow = self.table.currentIndex().row()
        productId = self.table.model().index(currentRow, 0).data()
        currentProduct = payload[productId]
        self.currentProductChanged.emit(currentProduct)

class LoadData(QObject):
    progress = pyqtSignal(dict)
    getAPIsStatus = pyqtSignal(bool)
    finished = pyqtSignal(dict)
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def run(self):
        self.getAPIsStatus.emit(False)
        response = _get('products', 'list')
        self.getAPIsStatus.emit(True)

        drive = Drive()
        if not os.path.exists(_getExactlyPath(PATH_FOLDER_OF_IMAGES)):
            os.mkdir(_getExactlyPath(PATH_FOLDER_OF_IMAGES))
        for product in response.values():
            for folderName in product[FOLDER_KEY]:
                fodlerPath = _getExactlyPath(PATH_FOLDER_OF_IMAGES + os.path.join(os.sep, folderName))
                if not os.path.exists(fodlerPath):
                    os.mkdir(fodlerPath)
                product['Folder path'] = fodlerPath
                del product[FOLDER_KEY]
                imagePaths = []
                for images in product[IMAGE_KEY]:
                    for imageName in images:
                        imagePath = fodlerPath + os.path.join(os.sep, imageName)    
                        imageId = images[imageName]
                        if not os.path.exists(imagePath):
                            drive._downloadImage(imageId, imagePath)
                        imagePaths.append(imagePath)
                product['Image path'] = imagePaths
                del product[IMAGE_KEY]
                self.progress.emit(product)
        self.finished.emit(response)

class SearchField(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setFixedWidth(900)

        self.centralLayout = QHBoxLayout()
        self.searchFieldId = QLineEdit()
        self.searchFieldId.setFixedWidth(100)
        self.searchFieldId.setPlaceholderText('ID')
        self.searchFieldCategory = QLineEdit()
        self.searchFieldCategory.setFixedWidth(100)
        self.searchFieldCategory.setPlaceholderText('Category')
        self.searchFieldWard = QLineEdit()
        self.searchFieldWard.setFixedWidth(100)
        self.searchFieldWard.setPlaceholderText('Ward')
        self.searchFieldStreetName = QLineEdit()
        self.searchFieldStreetName.setFixedWidth(100)
        self.searchFieldStreetName.setPlaceholderText('Street name')
        self.searchFieldAcreage = QLineEdit()
        self.searchFieldAcreage.setFixedWidth(100)
        self.searchFieldAcreage.setPlaceholderText('Acreage')
        self.searchFieldPrice = QLineEdit()
        self.searchFieldPrice.setFixedWidth(100)
        self.searchFieldPrice.setPlaceholderText('Price')
        self.searchFieldLegal = QLineEdit()
        self.searchFieldLegal.setFixedWidth(100)
        self.searchFieldLegal.setPlaceholderText('Legal')
        self.searchFieldBuildingLine = QLineEdit()
        self.searchFieldBuildingLine.setFixedWidth(100)
        self.searchFieldBuildingLine.setPlaceholderText('Building Line')

        self.centralLayout.addWidget(self.searchFieldId)
        self.centralLayout.addWidget(self.searchFieldCategory)
        self.centralLayout.addWidget(self.searchFieldWard)
        self.centralLayout.addWidget(self.searchFieldStreetName)
        self.centralLayout.addWidget(self.searchFieldAcreage)
        self.centralLayout.addWidget(self.searchFieldPrice)
        self.centralLayout.addWidget(self.searchFieldLegal)
        self.centralLayout.addWidget(self.searchFieldBuildingLine)
        self.setLayout(self.centralLayout)

class SortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, *args, **kwargs):
        QSortFilterProxyModel.__init__(self, *args, **kwargs)
        self.filters = {}

    def setFilterByColumn(self, regex, column):
        self.filters[column] = regex
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        for key, regex in self.filters.items():
            ix = self.sourceModel().index(source_row, key, source_parent)
            if ix.isValid():
                text = self.sourceModel().data(ix)
                if regex not in text:
                    return False
        return True

class LoadingScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 200)

        self.labelAnimation = QLabel(self)
        self.movie = QMovie(_getExactlyPath(PATH_LOADING_ANIMATION))
        self.labelAnimation.setMovie(self.movie)
        self.movie.start()