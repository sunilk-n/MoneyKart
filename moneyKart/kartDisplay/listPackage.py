import os
import sys
from PySide2 import QtWidgets, QtCore, QtGui

from moneyKart.kartDisplay import ui, pyQtUtils, iconPack
# from moneyKart.kartCal import spendEarn
from moneyKart.kartCal.utils import *

iconPath = iconPack.__path__[0]


class ListPackage(QtWidgets.QWidget):
    def __init__(self, parent=None, spendEarns=[], payment=None):
        super(ListPackage, self).__init__(parent)
        self.parent = parent
        innerStyle = """
            QPushButton:hover{
                background: #1E1F26;
            }
            #amountWidget{
                background: #283655;
            }
        """
        self.setAttribute(QtCore.Qt.WA_StyledBackground)

        widgetsList = AmountWidgets(self, spendEarns, payment=payment)
        widgetsList.setObjectName("amountWidget")
        widgetsList.setStyleSheet(innerStyle)
        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(widgetsList)
        scroll.setWidgetResizable(True)
        scroll.verticalScrollBar().setVisible(False)

        layout = QtWidgets.QVBoxLayout(self)
        pyQtUtils.setLayoutAttr(layout)
        layout.addWidget(scroll)

        self.setObjectName("listWidget")

        style = """
            QWidget{
                border: 0;
            }
            #listWidget{
              background: #283655;
            }
        """
        self.setStyleSheet(style)

    def updateSize(self):
        mainWindowSize = self.parent.frameGeometry()

        # self.width, self.height = (3 * mainWindowSize.width()) / 4, mainWindowSize.height()
        # maxWidth = self.width - 210
        # minWidth = self.width - (maxWidth / 2)
        # if self.width > maxWidth:
        #     self.width = maxWidth
        # elif self.width < minWidth:
        #     self.width = minWidth
        # self.resize(self.width, self.height)



class AmountWidgets(QtWidgets.QWidget):
    def __init__(self, parent=None, spendEarns=[], payment=None):
        super(AmountWidgets, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_StyledBackground)

        layout = QtWidgets.QVBoxLayout()
        pyQtUtils.setLayoutAttr(layout)

        for spendEarn in spendEarns:
            transaction = TransactionWidget(self, spendEarn, payment=payment)
            transaction.setObjectName('transaction')
            # group = transaction.createGroup(spendEarn.type, transaction)
            layout.addWidget(transaction)
            transaction.setAttribute(QtCore.Qt.WA_StyledBackground)
            style = """
                        #transaction{
                            background: #283655;
                            color: #D0E7F9;
                            border: 0;
                            padding-bottom: 15px;
                        }
                        #transaction:hover{
                            background: #4D648D;
                        }
                        QGroupBox{
                            border: 1px solid gray;
                            border-color: #D0E7F9;
                            font-size:14px;
                            margin-top: 10px;
                            border-radius: 10px;
                            color: #D0E7F9;
                        }
                        QGroupBox::title{
                            margin-top: -20px;
                        }
                        QLabel{
                            color: #D0E7F9;
                            padding: 5px;
                        }
                        QPushButton:hover{
                            background: #283655;
                            border-radius: 5px;
                        }
                        QMenu{
                            background: #283655;
                            color: #D0E7F9;
                            padding-top: 10px;
                            padding-left: 0;
                        }
                        QMenu::item:selected{
                            color: #283655;
                            background: #D0E7F9;
                        }
                    """
            transaction.setStyleSheet(style)
        layout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        self.setLayout(layout)

    def createGroup(self, name, widget):
        groupWidget = QtWidgets.QGroupBox()
        groupWidget.setTitle(name)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(widget)
        groupWidget.setLayout(layout)
        return groupWidget

    def returnId(self):
        print("Testing")

class TransactionWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, details=None, payment=None):
        super(TransactionWidget, self).__init__(parent)

        self.spendEarn = details
        self.payment = payment
        self.initUI()

        if self.spendEarn:
            self.setAmount(self.spendEarn.amount)
            if self.spendEarn.type == 'earn':
                self.amountLabel.setStyleSheet("color: #11FF22;")
            elif self.spendEarn.type == 'spend' and self.spendEarn.setType == 'bill':
                self.amountLabel.setStyleSheet("color: #FFDD11;")
            else:
                self.amountLabel.setStyleSheet("color: #FF1122;")
            self.setDate(self.spendEarn.date)
            self.setComment(self.spendEarn.comment)

    def initUI(self):
        self.amountLabel = QtWidgets.QLabel(self)
        self.dateLabel = QtWidgets.QLabel(self)
        self.commentLabel = QtWidgets.QLabel(self)
        self.optionsBtn = QtWidgets.QPushButton(self)

        # Create group boxes for display widgets
        amountGroup = self.createGroup("%s Amount" % self.spendEarn.type, self.amountLabel)
        dateGroup = self.createGroup("On Date", self.dateLabel)
        commentGroup = self.createGroup("Transaction for %s" % self.spendEarn.setType, self.commentLabel)

        # self.optionsBtn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # self.optionsBtn.customContextMenuRequested.connect(self.optionsWidget)
        self.optionsBtn.clicked.connect(self.optionsWidget)

        # Internal widget options
        amountFont = QtGui.QFont()
        amountFont.setPointSize(16)
        amountFont.setBold(True)
        self.amountLabel.setFont(amountFont)
        dateFont = QtGui.QFont()
        dateFont.setItalic(True)
        dateFont.setPointSize(10)
        dateFont.setBold(True)
        self.dateLabel.setFont(dateFont)
        self.dateLabel.setAlignment(QtCore.Qt.AlignCenter)
        commentFont = QtGui.QFont()
        commentFont.setPointSize(12)
        self.commentLabel.setFont(commentFont)
        self.commentLabel.setWordWrap(True)
        self.optionsBtn.setStyleSheet("width: 25px; height: 25px; max-width:25px; border:0;")
        self.optionsBtn.setIcon(QtGui.QPixmap(os.path.join(iconPath, 'options.png')))

        layout = QtWidgets.QGridLayout()
        pyQtUtils.setLayoutAttr(layout, 5, 2)
        layout.addWidget(amountGroup, 0, 0)
        layout.addWidget(dateGroup, 0, 1)
        layout.addWidget(self.optionsBtn, 0, 2)
        layout.addWidget(commentGroup, 1, 0, 1, 3)
        self.setLayout(layout)

    def optionsWidget(self):
        point = QtCore.QPoint()
        optionsMenu = QtWidgets.QMenu(self)
        editAction = QtWidgets.QAction("Edit", self)
        editAction.triggered.connect(self.editTransaction)
        delAction = QtWidgets.QAction("Delete",self)
        delAction.triggered.connect(self.deleteTransaction)
        optionsMenu.addAction(editAction)
        optionsMenu.addAction(delAction)
        optionsMenu.exec_(self.optionsBtn.mapToGlobal(point))

    def editTransaction(self):
        self.payment.connectPayment.emit(self.getId(), self.getType())

    def deleteTransaction(self):
        self.payment.connectDel.emit(self.getId(), self.getType())

    def createGroup(self, name, widget):
        groupWidget = QtWidgets.QGroupBox()
        groupWidget.setTitle(name)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(widget)
        groupWidget.setLayout(layout)
        return groupWidget

    def getId(self):
        if self.spendEarn:
            return self.spendEarn.id

    def getType(self):
        return self.spendEarn.type

    def setAmount(self, amount):
        prefix = "₹"
        amountFormat = "%s %0.2f" % (prefix, amount)
        self.amountLabel.setText(amountFormat)

    def setDate(self, date):
        self.dateLabel.setText(convertToDate(date))

    def setComment(self, comment):
        self.commentLabel.setText(comment.replace('!!!','"'))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = ListPackage()
    # gui.setAmount(34000)
    # gui.setDate("08-08-2019")
    # gui.setComment("Movie snacks(O)")
    gui.show()
    sys.exit(app.exec_())
