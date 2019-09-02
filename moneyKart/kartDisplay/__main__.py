import sys
from PySide2.QtWidgets import QApplication

if __name__ == '__main__':
    from moneyKart.kartDisplay.moneyKartUi import MoneyKart

    app = QApplication(sys.argv)
    gui = MoneyKart()
    gui.show()
    sys.exit(app.exec_())