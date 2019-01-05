# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-10 21:32:24
@Desc: 管理pin
"""


from .idmgr import GetIDMgr
from . import basemgr

g_PinMgr = None


def GetPinMgr():
    global g_PinMgr
    if not g_PinMgr:
        g_PinMgr = CPinMgr()
    return g_PinMgr


class CPinMgr(basemgr.CBaseMgr):

    def NewPin(self, pinID, oPin):
        self.m_ItemInfo[pinID] = oPin

    def DelPin(self, pinID):
        self.DelItem(pinID)
        GetIDMgr().DelPin(pinID)
