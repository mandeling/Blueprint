# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-14 14:42:48
@Desc: 
"""

from PyQt5 import QtCore

g_Signal = None

def GetSignal():
    global g_Signal
    if not g_Signal:
        g_Signal = CSignal()
    return g_Signal

class CSignal(QtCore.QObject):
    # 打开变量
    VARIABLE_OPEN = QtCore.pyqtSignal("PyQt_PyObject")
    # 改变变量名
    VARIABLE_CHANGE_NAME = QtCore.pyqtSignal("PyQt_PyObject")
    # 改变变量类型
    VARIABLE_CHANGE_TYPE = QtCore.pyqtSignal("PyQt_PyObject", "PyQt_PyObject")
    # 改变变量值
    VARIABLE_CHANGE_VALUE = QtCore.pyqtSignal("PyQt_PyObject", "PyQt_PyObject")

