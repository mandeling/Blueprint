# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-02 16:16:21
@Desc: 信号管理
"""

from pubcode.pubsignal import CMySignal

g_Signal = None


def GetSignal():
    global g_Signal
    if not g_Signal:
        g_Signal = CSignal()
    return g_Signal


class CSignal:
    # 数据层信号
    DEL_LINE = CMySignal()  # graphicID, lineID
    
    DEL_NODE = CMySignal()  # graphicID, nodeID
    NEW_NODE = CMySignal()  # graphicID, nodeID

    NEW_VARIABLE = CMySignal()  # bpID, varID
    NEW_GRAPHIC = CMySignal()   # bpID, graphicID

    # ui层信号
    # --蓝图--
    UI_NEW_BLUEPRINT = CMySignal()   # bpID
    UI_SHOW_BP_SEARCH = CMySignal()  # bpID
    UI_SAVE_BLUEPRINT = CMySignal()  # bpID
    UI_OPEN_BLUEPRINT = CMySignal()  # bpID

    # --图表--
    UI_FOCUS_GRAPHIC = CMySignal()  # bpID, graphicID
    UI_FOCUS_NODE = CMySignal()     # graphicID, nodeID

    # --变量--
    UI_OPEN_VARIABLE_DETAIL = CMySignal()  # bpID, varID
    UI_VARIABLE_CHANGE_ATTR = CMySignal()  # varID, attrName, value
