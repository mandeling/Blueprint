# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-11-08 16:43:10
@Desc: 主函数
"""

import sys
import os
import logging
import mainwindow

from PyQt5 import QtWidgets, QtGui

from ui import res_rc
from bpdata import node

from pubcode.pubfunc import pubmisc


def InitDir():
    for sDir in ("bpfile", "log"):
        if os.path.exists(sDir):
            continue
        os.makedirs(sDir)


def InitConfig():
    sys.excepthook = pubmisc.SysExceptHook

    sTime = pubmisc.Time2Str(timeformat="%Y-%m-%d")
    sLogName = os.path.join("log", sTime+".log")
    handler = logging.FileHandler(filename=sLogName, mode="a", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s - %(filename)s(%(lineno)d) - %(levelname)s - %(message)s"))
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    logger.addHandler(ch)


def Start():
    InitDir()
    InitConfig()
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
