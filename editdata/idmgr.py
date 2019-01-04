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
        self.m_BPNodeInfo = {}  # {bpID:[nodeID,]}
        self.m_Node2BP = {}     # {nodeID:bpID}
        self.m_NodePinInfo = {}  # {nodeID:[pinID,]}
        self.m_Pin2Node = {}    # {pinID:nodeID}
        self.m_PinLineInfo = {}  # {pinid:[lineid,]}
        self.m_BPLineInfo = {}  # {bpID:[lineID,]}
        self.m_Line2BP = {}     # {lineID:bpID}

    # ---------------------蓝图---------------------------
    def DelPB(self, bpID):
        for nodeID in self.m_BPNodeInfo[bpID]:
            self.DelNode(nodeID)
        del self.m_BPNodeInfo[bpID]

    def GetBPIDByNodeID(self, nodeID):
        return self.m_Node2BP[nodeID]

    # ----------------------节点--------------------------
    def NewNode(self, bpID, nodeID):
        lst = self.m_BPNodeInfo.setdefault(bpID, [])
        if nodeID not in lst:
            lst.append(nodeID)
        self.m_Node2BP[nodeID] = bpID

    def DelNode(self, nodeID):
        # 删除引脚槽
        for pinID in self.m_NodePinInfo[nodeID]:
            del self.m_Pin2Node[pinID]
        del self.m_NodePinInfo[nodeID]

        # 删除节点
        bpID = self.m_Node2BP[nodeID]
        lst = self.m_BPNodeInfo.setdefault(bpID, [])
        if nodeID not in lst:
            lst.remove(nodeID)
        del self.m_Node2BP[nodeID]

    def GetNodeIDByPinID(self, pinID):
        return self.m_Pin2Node[pinID]

    # -----------------------引脚-------------------------
    def NewPin(self, nodeID, pinID):
        lst = self.m_NodePinInfo.setdefault(nodeID, [])
        if pinID not in lst:
            lst.append(pinID)
        self.m_Pin2Node[pinID] = nodeID

    # ------------------------连线------------------------
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
