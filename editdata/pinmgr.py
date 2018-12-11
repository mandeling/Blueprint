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
        self.m_LineInfo = {}
        self.m_PinInfo = {}

    def NewPin(self, bpID, nodeID, pinID):
        dLineBPInfo = self.m_LineInfo.setdefault(bpID, {})
        dLineNodeInfo = dLineBPInfo.setdefault(nodeID, {})
        dLineNodeInfo.setdefault(pinID, [])

        dPinBPInfo = self.m_PinInfo.setdefault(bpID, {})
        dPinNodeInfo = dPinBPInfo.setdefault(nodeID, {})
        dPinNodeInfo.setdefault(pinID, [])

    def NewLine(self, bpID, oNodeID, oPinID, iNodeID, iPinID, lineID):
        self.m_LineInfo[bpID][oNodeID][oPinID].append(lineID)
        self.m_LineInfo[bpID][iNodeID][iPinID].append(lineID)

        self.m_PinInfo[bpID][oNodeID][oPinID].append((iNodeID, iPinID))
        self.m_PinInfo[bpID][iNodeID][iPinID].append((oNodeID, oPinID))

    def DelLine(self, bpID, oNodeID, oPinID, iNodeID, iPinID, lineID):
        self.m_LineInfo[bpID][oNodeID][oPinID].remove(lineID)
        self.m_LineInfo[bpID][iNodeID][iPinID].remove(lineID)

        self.m_PinInfo[bpID][oNodeID][oPinID].remove((iNodeID, iPinID))
        self.m_PinInfo[bpID][iNodeID][iPinID].remove((oNodeID, oPinID))

    def GetAllLineByPin(self, bpID, nodeID, pinID):
        return self.m_LineInfo[bpID][nodeID][pinID]

    def GetAllConnectPin(self, bpID, nodeID, pinID):
        return self.m_PinInfo[bpID][nodeID][pinID]
