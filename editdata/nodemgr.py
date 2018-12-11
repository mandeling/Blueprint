# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-07 16:13:20
@Desc: 节点管理
"""

import copy
from .import define

g_NodeMgr = None


def GetNodeMgr():
    global g_NodeMgr
    if not g_NodeMgr:
        g_NodeMgr = CNodeMgr()
    return g_NodeMgr


class CNodeMgr:
    def __init__(self):
        self.m_Info = {}
        self.m_DefineInfo = {}  # 节点定义的信息
        self.m_InputMap = {}    # 输入ID和pid映射

    # --------------定义节点的信息-----------------------
    def Register(self, sNodeName, info):
        """注册定义的节点"""
        self.m_DefineInfo[sNodeName] = info

    def BindInputID(self, sNodeName, iInputID, pid):
        dInfo = self.m_InputMap.setdefault(sNodeName, {})
        dInfo[iInputID] = pid

    def GetValue(self, sNodeName, iInputID):
        # TODO
        return 0

    def GetAllPin(self, sNodeName):
        dInfo = self.m_DefineInfo[sNodeName]
        return copy.deepcopy(dInfo)

    def GetAllDefineNodeName(self):
        return self.m_DefineInfo.keys()

    # ----------------编辑器节点信息-----------------------------
    def NewBlueprint(self, bpID):
        self.m_Info[bpID] = CBpNodeMgr()

    def NewNode(self, bpID, sNodeName):
        oBpNode = self.m_Info[bpID]
        return oBpNode.NewNode(sNodeName)

    def DelNode(self, bpID, nodeID):
        from . import interface
        from graphics import graphinterface
        lstLine = interface.GetAllLineByNode(bpID, nodeID)
        for lineID in lstLine:
            graphinterface.DelLine(bpID, lineID)
        oBpNode = self.m_Info[bpID]
        oBpNode.DelNode(nodeID)

    def GetNode(self, bpID, nodeID):
        oBpNode = self.m_Info[bpID]
        oNode = oBpNode.GetNode(nodeID)
        return oNode

    def SetNodeAttr(self, bpID, nodeID, sAttrName, value):
        oNode = self.GetNode(bpID, nodeID)
        oNode.SetAttr(sAttrName, value)

    def GetNodeAttr(self, bpID, nodeID, sAttrName):
        oNode = self.GetNode(bpID, nodeID)
        return oNode.GetAttr(sAttrName)


class CBpNodeMgr:
    def __init__(self):
        self.m_ID = 0
        self.m_Info = {}

    def NewID(self):
        self.m_ID += 1
        return self.m_ID

    def GetNode(self, nodeID):
        return self.m_Info[nodeID]

    def NewNode(self, sNodeName):
        uid = self.NewID()
        self.m_Info[uid] = CNode(uid, sNodeName)
        return uid

    def DelNode(self, uid):
        del self.m_Info[uid]


class CNode:
    def __init__(self, uid, sNodeName):
        self.m_Info = {
            define.NodeAttrName.ID: uid,
            define.NodeAttrName.NAME: sNodeName,
            define.NodeAttrName.POSITION: (0, 0),
            define.NodeAttrName.PININFO: GetNodeMgr().GetAllPin(sNodeName)
        }

    def SetAttr(self, sAttrName, value):
        self.m_Info[sAttrName] = value

    def GetAttr(self, sAttrName):
        return self.m_Info[sAttrName]
