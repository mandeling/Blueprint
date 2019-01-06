# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-29 10:19:16
@Desc: 保存各id直接的关系
"""

g_IDMgr = None


def GetIDMgr():
    global g_IDMgr
    if not g_IDMgr:
        g_IDMgr = CIDMgr()
    return g_IDMgr


def MyListAppend(dInfo, key, value):
    lst = dInfo.setdefault(key, [])
    if value not in lst:
        lst.append(value)


def MyListRemove(dInfo, key, value):
    lst = dInfo.setdefault(key, [])
    if value in lst:
        lst.remove(value)


class CIDMgr:
    def __init__(self):
        self.m_Node2BP = {}     # {nodeID:bpID}
        self.m_NodePinInfo = {}  # {nodeID:[pinID,]}
        self.m_Pin2Node = {}    # {pinID:nodeID}
        self.m_PinLineInfo = {}  # {pinid:[lineid,]}
        self.m_BPLineInfo = {}  # {bpID:[lineID,]}
        self.m_Line2BP = {}     # {lineID:bpID}

    # ---------------------节点ID:蓝图ID---------------------------
    def SetNode2BP(self, bpID, nodeID):
        self.m_Node2BP[nodeID] = bpID

    def DelNode4BP(self, nodeID):
        if nodeID in self.m_Node2BP:
            del self.m_Node2BP[nodeID]

    def GetBPByNode(self, nodeID):
        return self.m_Node2BP[nodeID]

    # ----------------------引脚ID:节点ID--------------------------
    def GetNodeIDByPinID(self, pinID):
        return self.m_Pin2Node[pinID]

    # -----------------------引脚-------------------------
    def SetPin2Node(self, nodeID, pinID):
        MyListAppend(self.m_NodePinInfo, nodeID, pinID)
        self.m_Pin2Node[pinID] = nodeID

    def DelPin(self, pinID):
        if pinID not in self.m_Pin2Node:
            return
        nodeID = self.m_Pin2Node[pinID]
        MyListRemove(self.m_NodePinInfo, nodeID, pinID)
        del self.m_Pin2Node[pinID]

    # ------------------------连线ID:蓝图ID------------------------
    def SetLine2BP(self, lineID, bpID):
        self.m_Line2BP[lineID] = bpID

    def GetBPByLine(self, lineID):
        return self.m_Line2BP.get(lineID, None)

    def DelLine2BP(self, lineID):
        if lineID in self.m_Line2BP:
            del self.m_Line2BP[lineID]

    def GetAllLineByPin(self, pinID):
        return self.m_PinLineInfo.get(pinID, [])

    def AddLine2BP(self, bpID, lineID):
        MyListAppend(self.m_BPLineInfo, bpID, lineID)
        self.m_Line2BP[lineID] = bpID

    def DelLine(self, lineID):
        bpID = self.m_Line2BP[lineID]
        MyListRemove(self.m_BPLineInfo, bpID, lineID)
        del self.m_Line2BP[lineID]

    # ------------------------引脚和连线------------------------
    def NewPinLine(self, oPinID, iPinID, lineID):
        MyListAppend(self.m_PinLineInfo, oPinID, lineID)
        MyListAppend(self.m_PinLineInfo, iPinID, lineID)

    def DelPinLine(self, oPinID, iPinID, lineID):
        self.m_PinLineInfo[oPinID].remove(lineID)
        self.m_PinLineInfo[iPinID].remove(lineID)
