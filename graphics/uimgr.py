# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-10 10:34:20
@Desc: ui界面管理
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
        self.m_PinUI = {}
        self.m_LineUI = {}

    def AddBPView(self, bpID, oBPView):
        self.m_BPUI[bpID] = weakref.ref(oBPView)

    def DelBPView(self, bpID):
        del self.m_BPUI[bpID]

    def GetBPView(self, bpID):
        return self.m_BPUI[bpID]()

    def AddNodeUI(self, nodeID, oNodeUI):
        self.m_NodeUI[nodeID] = weakref.ref(oNodeUI)

    def DelNodeUI(self, nodeID):
        if nodeID in self.m_NodeUI:
            del self.m_NodeUI[nodeID]

    def GetNodeUI(self, nodeID):
        if nodeID in self.m_NodeUI:
            return self.m_NodeUI[nodeID]()
        return None

    def AddPinUI(self, bpID, nodeID, pinID, oPinUI):
        dBPInfo = self.m_PinUI.setdefault(bpID, {})
        dNodeInfo = dBPInfo.setdefault(nodeID, {})
        dNodeInfo[pinID] = weakref.ref(oPinUI)

    def DelPinUI(self, bpID, nodeID, pinID):
        del self.m_PinUI[bpID][nodeID][pinID]

    def AddPinBtnUI(self, bpID, nodeID, pinID, oPinbtnUI):
        dBPInfo = self.m_PinBtnUI.setdefault(bpID, {})
        dNodeInfo = dBPInfo.setdefault(nodeID, {})
        dNodeInfo[pinID] = weakref.ref(oPinbtnUI)

    def DelPinBtnUI(self, bpID, nodeID, pinID):
        del self.m_PinBtnUI[bpID][nodeID][pinID]

    def AddLineUI(self, bpID, lineID, oLineUI):
        dInfo = self.m_LineUI.setdefault(bpID, {})
        dInfo[lineID] = weakref.ref(oLineUI)

    def GetLineUI(self, bpID, lineID):
        return self.m_LineUI[bpID][lineID]()

    def DelLineUI(self, bpID, lineID):
        dInfo = self.m_LineUI.setdefault(bpID, {})
        if lineID in dInfo:
            del dInfo[lineID]
