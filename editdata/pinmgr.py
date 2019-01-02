# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-10 21:32:24
@Desc: 管理pin
"""

g_PinMgr = None


def GetPinMgr():
    global g_PinMgr
    if not g_PinMgr:
        g_PinMgr = CPinMgr()
    return g_PinMgr


class CPinMgr:
    def __init__(self):
        self.m_Info = {}    # 存放pin信息

    def NewPin(self, pinID, oPin):
        self.m_Info[pinID] = oPin

    def GetAttr(self, pinID, sAttrName):
        oPin = self.m_Info[pinID]
        return oPin.GetAttr(sAttrName)
