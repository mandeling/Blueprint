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
        self.m_Graphic2BP = {}  # {graphicID:bpID}
        self.m_Node2Graphic = {}     # {nodeID:graphicID}
        self.m_Pin2Node = {}    # {pinID:nodeID}
        self.m_PinLineInfo = {}  # {pinid:[lineid,]}
        self.m_Line2Graphic = {}     # {lineID:graphicID}
        self.m_Var2Graphic = {}      # {varID:graphicID}

    # ---------------------图表ID:蓝图ID---------------------------
    def SetGraphic2BP(self, bpID, graphicID):
        self.m_Graphic2BP[graphicID] = bpID

    def GetBPByGraphic(self, graphicID):
        bpID = self.m_Graphic2BP.get(graphicID, None)
        assert bpID is not None
        return bpID

    def DelGraphic2BP(self, graphicID):
        bpID = self.m_Graphic2BP.pop(graphicID, None)
        assert bpID is not None
        return bpID

    # ---------------------变量ID:图表ID---------------------------
    def SetVar2Graphic(self, graphicID, varID):
        self.m_Var2Graphic[varID] = graphicID

    def GetGraphicByVar(self, varID):
        graphicID = self.m_Var2Graphic.get(varID, None)
        assert graphicID is not None
        return graphicID

    def DelVar2Graphic(self, varID):
        graphicID = self.m_Var2Graphic.pop(varID, None)
        assert graphicID is not None
        return graphicID

    # ---------------------节点ID:图表ID---------------------------
    def SetNode2Graphic(self, graphicID, nodeID):
        self.m_Node2Graphic[nodeID] = graphicID

    def GetGraphicByNode(self, nodeID):
        graphicID = self.m_Node2Graphic[nodeID]
        assert graphicID is not None
        return graphicID

    def DelNode2Graphic(self, nodeID):
        graphicID = self.m_Node2Graphic.pop(nodeID, None)
        assert graphicID is not None
        return graphicID

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

    # ------------------------连线ID:图表ID------------------------
    def SetLine2Graphic(self, graphicID, lineID):
        self.m_Line2Graphic[lineID] = graphicID

    def GetGraphicByLine(self, lineID):
        graphicID = self.m_Line2Graphic.get(lineID, None)
        assert graphicID is not None
        return graphicID

    def DelLine2Graphic(self, lineID):
        graphicID = self.m_Line2Graphic.pop(lineID, None)
        assert graphicID is not None
        return graphicID

    # ------------------------引脚和连线------------------------
    def AddLine2Pin(self, oPinID, iPinID, lineID):
        MyListAppend(self.m_PinLineInfo, oPinID, lineID)
        MyListAppend(self.m_PinLineInfo, iPinID, lineID)

    def DelLine4Pin(self, oPinID, iPinID, lineID):
        MyListRemove(self.m_PinLineInfo, oPinID, lineID)
        MyListRemove(self.m_PinLineInfo, iPinID, lineID)

    def GetAllLineByPin(self, pinID):
        return self.m_PinLineInfo.get(pinID, [])
