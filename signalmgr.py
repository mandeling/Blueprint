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
    DEL_LINE = CMySignal()
