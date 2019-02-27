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
    LINE_RUN_STATUE = CMySignal()  # lineID, bRun

    DEL_NODE = CMySignal()  # graphicID, nodeID
    NEW_NODE = CMySignal()  # graphicID, nodeID

    NEW_VARIABLE = CMySignal()  # bpID, varID
    NEW_GRAPHIC = CMySignal()   # bpID, graphicID

    PIN_ADD_LINE = CMySignal()  # pinID
    PIN_DEL_LINE = CMySignal()  # pinID

    # ui层信号
    # --蓝图--
    UI_NEW_BLUEPRINT = CMySignal()   # bpID
    UI_SHOW_BP_SEARCH = CMySignal()  # bpID
    UI_SAVE_BLUEPRINT = CMySignal()  # bpID
    UI_SAVE_ALL_BLUEPRINT = CMySignal()
    UI_OPEN_BLUEPRINT = CMySignal()  # bpID, [sPath]

    # --图表--
    UI_FOCUS_GRAPHIC = CMySignal()  # bpID, graphicID
    UI_FOCUS_NODE = CMySignal()     # graphicID, nodeID

    # --变量--
    UI_VARIABLE_CHANGE_ATTR = CMySignal()  # varID, attrName, value

    # --连线--
    UI_LINE_PRESS = CMySignal()     # graphicID, startPinID
    UI_LINE_MOVE = CMySignal()      # graphicID
    UI_LINE_RELEASE = CMySignal()   # graphicID
    UI_LINE_CONNECT = CMySignal()   # graphicID, endPinID
