# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-11-08 16:43:10
@Desc: 主函数
"""

import sys
import mainwindow
import misc

from ui import res_rc
from bpdata import node
from PyQt5 import QtWidgets, QtGui


def Start():
    sys.excepthook = misc.HandleException
    Mainwindow()


def Mainwindow():
    app = QtWidgets.QApplication(sys.argv)
    obj = mainwindow.CMainWindow()
    QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
    palette = obj.palette()
    dPaletteInfo = {
        QtGui.QPalette.Base: (60, 58, 56),
        QtGui.QPalette.AlternateBase: (80, 80, 80),
        QtGui.QPalette.Window: (56, 56, 56),
        QtGui.QPalette.Text: (180, 180, 180),
        QtGui.QPalette.WindowText: (180, 180, 180),
        QtGui.QPalette.Button: (80, 80, 80),
        QtGui.QPalette.ButtonText: (180, 180, 180),
        QtGui.QPalette.Light: (80, 80, 80),
        QtGui.QPalette.Inactive: (150, 150, 150),
        QtGui.QPalette.Highlight: (150, 150, 150),
    }
    for oQT, tColor in dPaletteInfo.items():
        palette.setColor(oQT, QtGui.QColor(*tColor))
    obj.setPalette(palette)
    obj.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    Start()
