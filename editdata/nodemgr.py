# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-07 16:13:20
@Desc: 节点管理
"""

import copy
import misc

from .idmgr import GetIDMgr
from bpdata import define as bddefine

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

    # --------------定义节点的信息-----------------------
    def Register(self, sNodeName, oDefineNode):
        """注册定义的节点"""
        self.m_DefineInfo[sNodeName] = oDefineNode

    def GetAllDefineNodeName(self):
        return self.m_DefineInfo.keys()

    # ----------------编辑器节点信息-----------------------------
    def NewNode(self, bpID, sNodeName, pos):
        oDefineNode = self.m_DefineInfo[sNodeName]
        oNode = copy.deepcopy(oDefineNode)
        nodeID = misc.uuid()
        GetIDMgr().NewNode(bpID, nodeID)
        oNode.SetAttr(bddefine.NodeAttrName.ID, nodeID)
        oNode.SetAttr(bddefine.NodeAttrName.POSITION, pos)
        lstPin = []
        for _, otPin in oNode.m_PinInfo.items():
            pinID = misc.uuid()
            oPin = copy.deepcopy(otPin)
            oPin.SetAttr(bddefine.PinAttrName.ID, pinID)
            lstPin.append(pinID)
            GetIDMgr().NewPin(nodeID, pinID)
        oNode.SetAttr(bddefine.NodeAttrName.PINIDLIST, lstPin)
        self.m_Info[nodeID] = oNode
        return nodeID

    def DelNode(self, nodeID):
        oNode = self.m_Info.get(nodeID, None)
        if oNode:
            return
        oNode.Delete()
        del self.m_Info[nodeID]

    def SetNodeAttr(self, nodeID, sAttrName, value):
        oNode = self.m_Info.get(nodeID, None)
        if oNode:
            return
        oNode.SetAttr(sAttrName, value)

    def GetNodeAttr(self, nodeID, sAttrName):
        oNode = self.m_Info.get(nodeID, None)
        if oNode:
            return
        return oNode.GetAttr(sAttrName)
