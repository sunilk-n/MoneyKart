import sys
import ctypes
from PySide2 import QtWidgets, QtCore

from moneyKart import *
from moneyKart.kartDisplay.rootMenu import RootToolBar
from moneyKart.kartDisplay import pyQtUtils
from moneyKart.kartDisplay.listPackage import ListPackage
from moneyKart.kartDisplay.paymentMethod import PaymentMethods
from moneyKart.kartCal.spendEarn import GetSpendEarn


class MoneyKart(QtWidgets.QWidget):
    def __init__(self):
        super(MoneyKart, self).__init__()

        self.setWindowTitle("Money Kart v{}".format(version))
        w, h = ctypes.windll.user32.GetSystemMetrics(0)/2, ctypes.windll.user32.GetSystemMetrics(1)/2
        self.resize(w, h)

        self.initUi()

        self.cp = pyQtUtils.Communicate()
        self.cp.connectPayment.connect(self.processPaymentWidget)
        self.cp.connectDel.connect(self.deleteTransaction)

    def initUi(self):
        self.toolBar = RootToolBar(self)
        self.allTransactions = GetSpendEarn()
        # self.displayTransactions = ListPackage(self, self.allTransactions.spendEarns)
        self.displayTransactions = QtWidgets.QWidget(self)

        self.contentLayout = QtWidgets.QVBoxLayout()
        pyQtUtils.setLayoutAttr(self.contentLayout)
        self.displayTransactions.setLayout(self.contentLayout)

        self.displayTransactions.setObjectName("widgetHolder")
        self.displayTransactions.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.displayTransactions.setStyleSheet("#widgetHolder{ background: #283655; }")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.toolBar)
        layout.addWidget(self.displayTransactions)
        pyQtUtils.setLayoutAttr(layout)
        self.setLayout(layout)

        self.toolBar.homeBtn.clicked.connect(self.processHomeWidget)
        self.toolBar.statsBtn.clicked.connect(self.processStatsWidget)
        self.toolBar.billBtn.clicked.connect(self.processPaymentWidget)

    def resizeEvent(self, *args, **kwargs):
        self.toolBar.updateSize()
        # self.displayTransactions.updateSize()

    def widgetLayout(self, _widget):
        self.clearLayout(self.contentLayout)
        self.contentLayout.addWidget(_widget)

    def clearLayout(self, layout):
        if layout != None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clearLayout(child.layout())

    @pyQtUtils.showWaitCursor
    def deleteTransaction(self, *args):
        self.allTransactions.deleteEntry(args[0], args[1])
        self.processHomeWidget()

    @pyQtUtils.showWaitCursor
    def processHomeWidget(self):
        dashBoard = ListPackage(self, self.allTransactions.decendSpendEarns, payment=self.cp)
        self.widgetLayout(dashBoard)

    @pyQtUtils.showWaitCursor
    def processStatsWidget(self):
        self.allTransactions.updateData()
        self.widgetLayout(QtWidgets.QWidget(self))

    @pyQtUtils.showWaitCursor
    def processPaymentWidget(self, *args):
        if args:
            self.widgetLayout(PaymentMethods(self, id=args[0], type=args[1]))
        else:
            self.widgetLayout(PaymentMethods(self))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = MoneyKart()
    gui.show()
    gui.processHomeWidget()
    # gui.widgetLayout(ListPackage(gui, gui.allTransactions.spendEarns))
    sys.exit(app.exec_())
