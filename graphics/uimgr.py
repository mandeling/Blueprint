# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-10 10:34:20
@Desc: 
"""

import weakref

g_UIMgr = None


def GetUIMgr():
    global g_UIMgr
    if not g_UIMgr:
        g_UIMgr = CUIManager()
    return g_UIMgr


class CUIManager:
    def __init__(self):
        self.m_BPUI = {}
        self.m_NodeUI = {}
        self.m_PinBtnUI = {}
        self.m_PinUIUI = {}
        self.m_LineUI = {}

    def AddBPView(self, bpID, oBPView):
        self.m_BPUI[bpID] = weakref.ref(oBPView)

    def GetBPView(self, bpID):
        return self.m_BPUI[bpID]()

    def AddNodeUI(self, bpID, nodeID, oNodeUI):
        dInfo = self.m_NodeUI.setdefault(bpID, {})
        dInfo[nodeID] = weakref.ref(oNodeUI)

    def AddPinUI(self, bpID, nodeID, pinID, oPinUI):
        dBPInfo = self.m_PinUIUI.setdefault(bpID, {})
        dNodeInfo = dBPInfo.setdefault(nodeID, {})
        dNodeInfo[pinID] = weakref.ref(oPinUI)

    def AddPinBtnUI(self, bpID, nodeID, pinID, oPinbtnUI):
        dBPInfo = self.m_PinBtnUI.setdefault(bpID, {})
        dNodeInfo = dBPInfo.setdefault(nodeID, {})
        dNodeInfo[pinID] = weakref.ref(oPinbtnUI)

    def AddLineUI(self, bpID, lineID, oLineUI):
        dInfo = self.m_LineUI.setdefault(bpID, {})
        dInfo[lineID] = weakref.ref(oLineUI)

    def GetLineUI(self, bpID, lineID):
        return self.m_LineUI[bpID][lineID]()
