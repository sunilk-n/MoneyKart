from datetime import datetime
from PySide2 import QtWidgets
from PySide2.QtCharts import QtCharts
from PySide2.QtGui import QPainter,QFont, QPalette, QColor
from PySide2.QtCore import QPoint, Qt

from moneyKart.kartDisplay import pyQtUtils
from moneyKart.kartCal.spendEarn import GetSpendEarn
from moneyKart.kartCal import utils



class DashBoard(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(DashBoard, self).__init__(parent)

        total = TotalSpendsEarnsWidget(self)
        layout = QtWidgets.QGridLayout()
        pyQtUtils.setLayoutAttr(layout)
        layout.addWidget(total, 0, 0)
        layout.addItem(QtWidgets.QSpacerItem(20, 40,
                             QtWidgets.QSizePolicy.Minimum,
                             QtWidgets.QSizePolicy.Expanding),
                            1, 0)
        layout.addItem(QtWidgets.QSpacerItem(40, 20,
                             QtWidgets.QSizePolicy.Expanding,
                             QtWidgets.QSizePolicy.Minimum),
                            0, 1)

        self.setLayout(layout)


class GeneralStatusInfo(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(GeneralStatusInfo, self).__init__(parent)


class TotalSpendsEarnsWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TotalSpendsEarnsWidget, self).__init__(parent)

        style = """
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
        """

        self.spendGroup = QtWidgets.QGroupBox("Spends", self)
        self.earnGroup = QtWidgets.QGroupBox("Earns", self)

        spendEarn = GetSpendEarn()
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        # Spend data
        spendLayout = QtWidgets.QHBoxLayout()
        pyQtUtils.setLayoutAttr(spendLayout)
        spendWidget = QtWidgets.QLabel(self)
        spendWidget.setText(spendEarn.sumOfSpendEarn(datetime.today().month, 'spend'))
        spendWidget.setFont(font)
        spendLayout.addWidget(spendWidget)
        self.spendGroup.setLayout(spendLayout)
        # Earn data
        earnLayout = QtWidgets.QHBoxLayout()
        pyQtUtils.setLayoutAttr(earnLayout)
        earnWidget = QtWidgets.QLabel(self)
        earnWidget.setText(spendEarn.sumOfSpendEarn(datetime.today().month, 'earn'))
        earnWidget.setFont(font)
        earnLayout.addWidget(earnWidget)
        self.earnGroup.setLayout(earnLayout)

        layout = QtWidgets.QVBoxLayout()
        pyQtUtils.setLayoutAttr(layout)
        layout.addWidget(self.earnGroup)
        layout.addWidget(self.spendGroup)
        layout.addItem(QtWidgets.QSpacerItem(20, 40,
                         QtWidgets.QSizePolicy.Minimum,
                         QtWidgets.QSizePolicy.Expanding))

        # Chart for spends and earns
        spendEarnChart = SpendEarnLinesChart(spendEarn, self)

        mainLayout = QtWidgets.QHBoxLayout()
        pyQtUtils.setLayoutAttr(mainLayout)
        mainLayout.addWidget(spendEarnChart.chartView)
        mainLayout.addLayout(layout)

        self.setLayout(mainLayout)
        self.setStyleSheet(style)


class SpendEarnLinesChart(QtWidgets.QWidget):
    def __init__(self, spendEarnClass, parent=None):
        super(SpendEarnLinesChart, self).__init__(parent)

        style = """
            background: rgba(255, 255, 255, 0%);
        """

        self.setObjectName("TransactionChart")
        self.spendSeries = QtCharts.QLineSeries()
        self.spendSeries.setName("spends")
        today = datetime.today().day
        for index, dated in enumerate(utils.genearateDates(today)):
            self.spendSeries.append(
                    QPoint(index,
                           spendEarnClass.spendEarnByDate(dated, 'spend')
                           )
                )

        self.earnSeries = QtCharts.QLineSeries()
        self.earnSeries.setName("earns")
        for index, dated in enumerate(utils.genearateDates(today)):
            self.earnSeries.append(
                    QPoint(index,
                           spendEarnClass.spendEarnByDate(dated, 'earn')
                           )
                )

        self.chart = QtCharts.QChart()
        self.chart.addSeries(self.earnSeries)
        self.chart.addSeries(self.spendSeries)
        # self.chart.setTitle("Line charts for spends and earns")

        self.categories = [i for i in range(1, today+1)]
        self.axisX = QtCharts.QBarCategoryAxis()
        # self.axisX.append(self.categories)
        self.axisX.setVisible(False)
        self.chart.setAxisX(self.axisX, self.spendSeries)
        # self.axisX.setRange(1, today)
        #
        self.axisY = QtCharts.QValueAxis()
        self.axisY.setVisible(False)
        self.chart.setAxisY(self.axisY, self.earnSeries)
        self.axisY.setRange(0, max(spendEarnClass.spendEarnByList()) + 100)

        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)
        self.chart.setAnimationOptions(QtCharts.QChart.AllAnimations)

        self.chartView = QtCharts.QChartView(self.chart)
        self.chartView.setRenderHint(QPainter.Antialiasing)
        pal = QPalette()
        pal.setColor(QPalette.WindowText, QColor(255, 0, 0, 127))
        self.chartView.setPalette(pal)

        self.chartView.setStyleSheet(style)
        self.show()
