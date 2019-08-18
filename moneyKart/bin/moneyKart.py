from PySide2.QtWidgets import QApplication
import sys
sys.path.append("F:/Python softwares/moneyKart")

from moneyKart.kartDisplay.moneyKartUi import MoneyKart

app = QApplication(sys.argv)
gui = MoneyKart()
gui.show()
sys.exit(app.exec_())
