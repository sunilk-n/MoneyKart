from PySide2 import QtCore, QtWidgets, QtGui
import decorator

@decorator.decorator
def showWaitCursor(func, *args, **kwargs):
    QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
    try:
        func(*args, **kwargs)
    finally:
        QtWidgets.QApplication.restoreOverrideCursor()


def setLayoutAttr(layout, space=0, margin=0):
    layout.setSpacing(space)
    layout.setMargin(margin)

class Communicate(QtCore.QObject):
    connectPayment = QtCore.Signal(str, str)
    connectDel = QtCore.Signal(str, str)

class StatusUpdate(QtWidgets.QMessageBox):
    def __init__(self, parent=None, msgType="info", msg=None, title=None, info=None):
        super(StatusUpdate, self).__init__(parent)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.setText(msg)
        self.setWindowTitle(title)
        if msgType == "info":
            self.setIcon(self.Information)
        elif msgType == "warn":
            self.setIcon(self.Warning)
            self.setInformativeText(info)
        elif msgType == "error":
            self.setIcon(self.Critical)
            self.setDetailedText(info)

        grph = QtWidgets.QGraphicsDropShadowEffect()
        grph.setBlurRadius(5)
        self.setGraphicsEffect(grph)

        self.setStandardButtons(self.Ok)
        style = """
            background: #D0E7F9;
            color: #283655;
        """
        self.setStyleSheet(style)
        self.show()
