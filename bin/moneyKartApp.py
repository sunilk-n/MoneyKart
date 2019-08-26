from PySide2.QtWidgets import QApplication
import sys
import os

projectPath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(projectPath)

from moneyKart.kartDisplay.moneyKartUi import MoneyKart
from moneyKart import update

app = QApplication(sys.argv)
gui = MoneyKart()
if not update.checkForUpdates():
    gui.show()
sys.exit(app.exec_())
