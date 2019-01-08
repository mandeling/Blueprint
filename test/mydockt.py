# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-28 16:39:50
@Desc: 
"""

import sys

from PyQt5.QtWidgets import QMainWindow, QStyleFactory,\
    QWidget, QDockWidget, QSizePolicy, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor


class CMyWidget(QWidget):
    def __init__(self, sTitle, parent=None):
        super(CMyWidget, self).__init__(parent)
        self.setWindowTitle(sTitle)


class CMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(CMainWindow, self).__init__(parent)
        self.InitUI()
        self.InitCorner()
        self.InitDock()
        self.InitCenter()

    def InitUI(self):
        self.showMaximized()
        self.setWindowTitle("QDockWidget-Test")

    def InitCorner(self):
        self.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.TopRightCorner, Qt.RightDockWidgetArea)
        self.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)

    def InitDock(self):
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        topDock = QDockWidget("顶侧面板", self)
        topDock.setSizePolicy(sizePolicy)
        topDock.setObjectName("topDock")
        topDock.setWidget(CMyWidget("顶侧面板"))

        bottomDock = QDockWidget("底侧面板", self)
        bottomDock.setSizePolicy(sizePolicy)
        bottomDock.setObjectName("bottomDock")
        bottomDock.setWidget(CMyWidget("底侧面板"))

        leftDock = QDockWidget("左侧面板", self)
        leftDock.setSizePolicy(sizePolicy)
        leftDock.setObjectName("leftDock")
        leftDock.setWidget(CMyWidget("左侧面板"))

        rightDock = QDockWidget("右侧面板", self)
        rightDock.setSizePolicy(sizePolicy)
        rightDock.setObjectName("rightDock")
        rightDock.setWidget(CMyWidget("右侧面板"))

        self.addDockWidget(Qt.RightDockWidgetArea, rightDock)
        self.addDockWidget(Qt.TopDockWidgetArea, topDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, bottomDock)
        self.addDockWidget(Qt.LeftDockWidgetArea, leftDock)
        self.setCentralWidget(CMyWidget("中心控件"))

    def InitCenter(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    obj = CMainWindow()
    QApplication.setStyle(QStyleFactory.create("Fusion"))
    palette = obj.palette()
    dPaletteInfo = {
        QPalette.Base: (60, 58, 56),
        QPalette.AlternateBase: (80, 80, 80),
        QPalette.Window: (56, 56, 56),
        QPalette.Text: (180, 180, 180),
        QPalette.WindowText: (180, 180, 180),
        QPalette.Button: (80, 80, 80),
        QPalette.ButtonText: (180, 180, 180),
        QPalette.Light: (80, 80, 80),
        QPalette.Inactive: (150, 150, 150),
        QPalette.Highlight: (150, 150, 150),
    }
    for oQT, tColor in dPaletteInfo.items():
        palette.setColor(oQT, QColor(*tColor))
    obj.setPalette(palette)
    obj.show()
    sys.exit(app.exec_())
