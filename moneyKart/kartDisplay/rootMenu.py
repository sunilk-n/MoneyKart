import sys

from moneyKart.kartDisplay.iconPack import *
from moneyKart.kartDisplay.pyQtUtils import *


class RootToolBar(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(RootToolBar, self).__init__(parent)
        self.parent = parent
        self.btnStyle = """
                QPushButton{
                    border: 0;
                    height:100;
                    font-size: 18px;
                    color: #D0E7F9;
                    padding-left: 20px;
                    padding-right: 20px;
                }
                QPushButton:hover{
                    background: #283655;
                }
            """
        self.initUi()
        self.updateSize()
        style = "background: #1E1F26;"

        self.setStyleSheet(style)


    def updateSize(self):
        mainWindowSize = self.parent.frameGeometry()

        # self.width, self.height = mainWindowSize.width()/4, mainWindowSize.height()
        # maxWidth = 210
        # minWidth = maxWidth/2
        # if self.width > maxWidth:
        #     self.width = maxWidth
        # elif self.width < minWidth:
        #     self.width = minWidth
        # self.resize(self.width, self.height)

    def initUi(self):
        self.setAttribute(QtCore.Qt.WA_StyledBackground)

        self.homeBtn = ToolBarButton(self, text="Home")
        self.statsBtn = ToolBarButton(self, text="Stats")
        self.billBtn = ToolBarButton(self, text="Payments")
        self.homeBtn.setStyleSheet(self.btnStyle)
        self.statsBtn.setStyleSheet(self.btnStyle)
        self.billBtn.setStyleSheet(self.btnStyle)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.homeBtn)
        layout.addWidget(self.statsBtn)
        layout.addWidget(self.billBtn)
        layout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        setLayoutAttr(layout, 0, 0)
        self.setLayout(layout)



class ToolBarButton(QtWidgets.QPushButton):
    def __init__(self, parent, text="", icon=False, iconType='menu', style=None):
        super(ToolBarButton, self).__init__(parent)

        toolSize = parent.frameGeometry()
        width, height = toolSize.width(), toolSize.height()/7
        if icon:
            iconImg = getPixPack(iconType)
            self.setIcon(iconImg)
            width = height = toolSize.height()
            self.setIconSize(QtCore.QSize(width, height))
        else:
            label = text.upper()
            self.setText(label)

        btnStyle = "width: {}; height: {}px; font-size: 18px; font-weight: 400;"
        # print(width, height)
        self.setStyleSheet(btnStyle.format(width, height))


class CustomToolButton(QtWidgets.QWidget):
    def __init__(self, parent, iconType='menu', style=None):
        super(CustomToolButton, self).__init__(parent)

        toolSize = parent.frameGeometry()
        width, height = toolSize.width(), toolSize.height() / 7
        self.resize(width, height)
        menuBtn = ToolBarButton(self, icon=True, iconType=iconType)

        widgetStyle = "width: {0}; height: {1};"
        self.setStyleSheet(widgetStyle.format(width, height))

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(menuBtn)
        layout.addItem(
            QtWidgets.QSpacerItem(
                20, 40,
                QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Minimum
            )
        )
        setLayoutAttr(layout)
        self.setLayout(layout)

        self.setStyleSheet(style)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = RootToolBar()
    gui.show()
    sys.exit(app.exec_())
