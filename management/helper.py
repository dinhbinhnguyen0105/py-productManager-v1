import os
import json
import string
import shutil
import random
from datetime import datetime

URL_FOLDER_OF_IMAGES = 'py-production-management\\bin\\images'


def _getExactlyPath(targetURL, srcURL = 'py-production-management'):
    currentURL = os.path.join(__file__)
    while True:
        headTail = os.path.split(currentURL)
        currentURL = headTail[0]
        tail = headTail[1]
        if tail == srcURL:
            break
    return currentURL + os.sep + targetURL

def _importDataConfig(dataConfigUrl):
    url = _getExactlyPath(dataConfigUrl)
    try:
        with open(url, encoding='utf-8') as data_file:
            return json.load(data_file)
    except FileNotFoundError:
        print('ERROR: FileNotFoundError')
        return False

def _removeAccents(inputStr):
    s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
    s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
    s = ''
    for c in inputStr:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c
    return s

def _initFolderName(category='', street='', acreage='', price=''):
    _dtString = datetime.now().strftime('%H%M%S%m%d%Y')
    _category = _removeAccents(category).translate({ord(c): None for c in string.whitespace}).lower()
    _streetName = _removeAccents(street).translate({ord(c): None for c in string.whitespace}).lower()
    _acreage = acreage
    _price = price
    return f'{_category}_{_streetName}_{_acreage}_{_price}_{_dtString}'

def _createFolder(targetUrl='', folderName=''):
    if not os.path.exists(targetUrl):
        os.mkdir(targetUrl)
    count = 0
    while True:
        _folder = f'{targetUrl}{os.sep}{folderName}{count}'
        if not os.path.exists(_folder):
            os.mkdir(_folder)
            return _folder
        else:
            count += 1

def _copyImages(srcUrl = [], targetUrl = ''):
    count = 0
    result = []
    for image in srcUrl:
        imageName = f'{targetUrl.split(os.sep)[-1]}_{count}{os.path.splitext(image)[-1]}'
        count += 1
        imageUrl = f'{targetUrl}{os.sep}{imageName}'
        shutil.copy(image, imageUrl)
        result.append(imageUrl)
    return result

def _randomIcon(icons_str):
    index = random.randint(0, len(icons_str) - 1)
    return icons_str[index]

    pass