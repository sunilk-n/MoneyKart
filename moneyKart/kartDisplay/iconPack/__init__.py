from PySide2 import QtGui
import os

IMG_PACK = ['close', 'min', 'max', 'menu']

def getPixPack(pack='close'):
    imgPix = None
    for each in IMG_PACK:
        if each == pack:
            imgPath = os.path.join(
                        os.path.dirname(__file__),
                        '%s.png' % pack
                       )
            if os.path.exists(imgPath):
                pix = QtGui.QPixmap(imgPath)
                imgPix = QtGui.QIcon(pix)
            else:
                raise ValueError("Either application is not installed correctly or Image had been deleted.")
    if imgPix:
        return imgPix
    else:
        raise ValueError("{0} was not part of Image pack.\nPlease select from {1}".format(pack, IMG_PACK))
