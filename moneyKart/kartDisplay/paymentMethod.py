from PySide2 import QtWidgets, QtGui

from moneyKart.kartDisplay import pyQtUtils
from moneyKart.kartCal.utils import *
from moneyKart.kartCal.spendEarn import GetSpendEarn, SpendEarn

class PaymentMethods(QtWidgets.QWidget):
    def __init__(self, parent=None, id=None, type='spend'):
        super(PaymentMethods, self).__init__(parent)

        self._id = id
        self._type = type

        style = """
            QTextEdit{
                background: #4D648D;
                border-radius: 10px;
                padding: 5px;
                color: #D0E7F9;
                font-size:14px;
            }
            QLabel{
                color: #D0E7F9;
                font-size: 16px;
                padding: 5px;
            }
            QLineEdit, QDateEdit, QComboBox, QPushButton{
                background: #4D648D;
                color: #D0E7F9;
                font-size: 14px;
                padding: 5px;
                border: 0;
                border-radius: 5px;
            }
            QPushButton:hover{
                background: #2288FF;
            }
        """

        self.initUI()

        self.setStyleSheet(style)

    def initUI(self):
        self.allTransactions = GetSpendEarn()

        layout = QtWidgets.QGridLayout()
        pyQtUtils.setLayoutAttr(layout, margin=10, space=5)

        amountLabel = QtWidgets.QLabel("Amount", self)
        dateLabel = QtWidgets.QLabel("Date", self)
        commentLabel = QtWidgets.QLabel("Comment for transaction", self)
        typeLabel = QtWidgets.QLabel("Transaction type", self)
        catLabel = QtWidgets.QLabel("Category", self)

        self.amountHolder = QtWidgets.QLineEdit(self)
        self.commentHolder = QtWidgets.QTextEdit(self)
        self.dateHolder = QtWidgets.QDateEdit(self)
        self.typeHolder = QtWidgets.QComboBox(self)
        self.catHolder = QtWidgets.QComboBox(self)
        self.saveBtn = QtWidgets.QPushButton("Save", self)

        self.amountHolder.setValidator(QtGui.QDoubleValidator())
        self.amountHolder.setPlaceholderText("0")
        self.typeHolder.addItems(types)
        self.catHolder.addItems(seTypes)
        self.dateHolder.setDisplayFormat("dd/MM/yyyy")

        # Connections
        self.typeHolder.currentIndexChanged.connect(self.updateId)
        self.saveBtn.clicked.connect(self.addEntry)

        if self._id:
            transaction = self.allTransactions.data[self._type][str(self._id)]
            comment = transaction[0].split(': ')[-1]
            self.dateHolder.setDate(convertFromDate(transaction[2]))
            self.amountHolder.setText(str(transaction[1]))
            self.commentHolder.setText(comment)
            catIndex = self.catHolder.findText(transaction[-1])
            self.catHolder.setCurrentIndex(catIndex)

            self.typeHolder.setDisabled(True)
        else:
            self._id = None
            self.dateHolder.setDate(datetime.datetime.today())
        index = self.typeHolder.findText(self._type)
        self.typeHolder.setCurrentIndex(index)

        layout.addWidget(typeLabel, 0, 0)
        layout.addWidget(catLabel, 0, 2)
        layout.addWidget(amountLabel, 1, 0)
        layout.addWidget(dateLabel, 1, 2)
        layout.addWidget(commentLabel, 2, 0, 1, 4)

        layout.addWidget(self.typeHolder, 0, 1)
        layout.addWidget(self.catHolder, 0, 3)
        layout.addItem(
                            QtWidgets.QSpacerItem(40, 20,
                                               QtWidgets.QSizePolicy.Expanding,
                                               QtWidgets.QSizePolicy.Minimum),
                            0, 4
                         )
        layout.addWidget(self.amountHolder, 1, 1)
        layout.addWidget(self.dateHolder, 1, 3)
        layout.addWidget(self.commentHolder, 3, 0, 1, 5)
        layout.addItem(
                        QtWidgets.QSpacerItem(20, 40,
                                         QtWidgets.QSizePolicy.Minimum,
                                         QtWidgets.QSizePolicy.Expanding),
                        4, 0
                       )
        layout.addWidget(self.saveBtn, 5, 4)

        self.setLayout(layout)

    def updateId(self, type):
        self._type = types[type]

    def addEntry(self):
        errorMsg = []
        if self._id:
            prevCmnt = self.commentHolder.toPlainText().split(')')[-1]
            comment = "<b>Edited on {DATE}</b>: {COMMENT}".format(DATE=convertToDate(datetime.datetime.today()), COMMENT=prevCmnt)
        else:
            comment = self.commentHolder.toPlainText()
        if comment == "":
            errorMsg.append("Please provide the comment to save the transaction.")
        if self.amountHolder.text() == "":
            errorMsg.append("Please provide the amount of transaction.")
        if errorMsg:
            pyQtUtils.StatusUpdate(self, 'warn', "Please resolve the below issue:",
                                   info="\n".join(errorMsg), title="Issue")
            return
        entry = SpendEarn(
            id=self._id,
            comment=comment,
            type=self._type,
            setType=self.catHolder.currentText(),
            amount=self.amountHolder.text(),
            date=self.dateHolder.text()
          )
        addTransact = self.allTransactions.addSpendEarn(entry)
        if addTransact:
            self.resetTextEdits()
            self._id = None
            pyQtUtils.StatusUpdate(self, 'info', "Successfully saved the details.", title="Success")
            return
        else:
            pyQtUtils.StatusUpdate(self, 'warn', "Some issue raise for details entered", title="Issue")
            return


    def resetTextEdits(self):
        self.typeHolder.setCurrentIndex(0)
        self.catHolder.setCurrentIndex(0)
        self.amountHolder.setText("")
        self.dateHolder.setDate(datetime.datetime.today())
        self.commentHolder.setText("")

