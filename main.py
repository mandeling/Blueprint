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
from PyQt5 import QtWidgets


def Start():
    sys.excepthook = misc.HandleException
    Mainwindow()


def Mainwindow():
    app = QtWidgets.QApplication(sys.argv)
    obj = mainwindow.CMainWindow()
    obj.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    Start()
