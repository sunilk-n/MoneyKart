from PySide2.QtWidgets import QApplication
import sys
import os

projectPath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(projectPath)

from moneyKart.kartDisplay.moneyKartUi import MoneyKart

app = QApplication(sys.argv)
gui = MoneyKart()
gui.show()
sys.exit(app.exec_())
