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
        self.m_Pin2Node = {}    # {pinID:nodeID}
        self.m_PinLineInfo = {}  # {pinid:[lineid,]}
        self.m_Line2BP = {}     # {lineID:bpID}
        self.m_Var2BP = {}      # {varID:bpID}

    # ---------------------变量ID:蓝图ID---------------------------
    def SetVar2BP(self, bpID, varID):
        self.m_Var2BP[varID] = bpID

    def GetBPByVar(self, varID):
        bpID = self.m_Var2BP.get(varID, None)
        assert bpID is not None
        return bpID

    def DelVar2BP(self, varID):
        bpID = self.m_Var2BP.pop(varID, None)
        assert bpID is not None
        return bpID

    # ---------------------节点ID:蓝图ID---------------------------
    def SetNode2BP(self, bpID, nodeID):
        self.m_Node2BP[nodeID] = bpID

    def GetBPByNode(self, nodeID):
        bpID = self.m_Node2BP[nodeID]
        assert bpID is not None
        return bpID

    def DelNode2BP(self, nodeID):
        bpID = self.m_Node2BP.pop(nodeID, None)
        assert bpID is not None
        return bpID

    # ----------------------引脚ID:节点ID--------------------------
    def SetPin2Node(self, nodeID, pinID):
        self.m_Pin2Node[pinID] = nodeID

    def GetNodeByPin(self, pinID):
        nodeID = self.m_Pin2Node.get(pinID, None)
        assert nodeID is not None
        return nodeID

    def DelPin2Node(self, pinID):
        nodeID = self.m_Pin2Node.pop(pinID, None)
        assert nodeID is not None
        return nodeID

    # ------------------------连线ID:蓝图ID------------------------
    def SetLine2BP(self, bpID, lineID):
        self.m_Line2BP[lineID] = bpID

    def GetBPByLine(self, lineID):
        bpID = self.m_Line2BP.get(lineID, None)
        assert bpID is not None
        return bpID

    def DelLine2BP(self, lineID):
        bpID = self.m_Line2BP.pop(lineID, None)
        assert bpID is not None
        return bpID

    # ------------------------引脚和连线------------------------
    def AddLine2Pin(self, oPinID, iPinID, lineID):
        MyListAppend(self.m_PinLineInfo, oPinID, lineID)
        MyListAppend(self.m_PinLineInfo, iPinID, lineID)

    def DelLine4Pin(self, oPinID, iPinID, lineID):
        MyListRemove(self.m_PinLineInfo, oPinID, lineID)
        MyListRemove(self.m_PinLineInfo, iPinID, lineID)

    def GetAllLineByPin(self, pinID):
        return self.m_PinLineInfo.get(pinID, [])
