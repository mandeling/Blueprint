# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-10 21:32:24
@Desc: 
"""


g_PinMgr = None


def GetLineMgr():
    global g_PinMgr
    if not g_PinMgr:
        g_PinMgr = CPinMgr()
    return g_PinMgr


class CPinMgr:
    def __init__(self):
        self.m_Info = {}

    def NewPin(self, bpID, nodeID, pinID):
        self.m_Info[bpID] = {}
        self.m_Info[bpID][nodeID] = {}
        self.m_Info[bpID][pinID] = []

    def NewLine(self, bpID, oNodeID, oPinID, iNodeID, iPinID):
        self.m_Info[bpID][oNodeID][oPinID].append((iNodeID, iPinID))
        self.m_Info[bpID][iNodeID][iPinID].append((oNodeID, oPinID))

    def DelLine(self, bpID, oNodeID, oPinID, iNodeID, iPinID):
        oInfo = (oNodeID, oPinID)
        if oInfo in self.m_Info[bpID][iNodeID][iPinID]:
            del self.m_Info[bpID][iNodeID][iPinID][oInfo]
        iInfo = ((iNodeID, iPinID))
        if iInfo in self.m_Info[bpID][oNodeID][oPinID]:
            del self.m_Info[bpID][oNodeID][oPinID][iInfo]
