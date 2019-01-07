# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-07 16:13:20
@Desc: 节点管理
"""

import copy
import misc

from . import interface
from .idmgr import GetIDMgr
from .pinmgr import GetPinMgr
from bpdata import define as bddefine
from signalmgr import GetSignal
from . import basemgr
from .bpmgr import GetBPMgr

g_NodeMgr = None


def GetNodeMgr():
    global g_NodeMgr
    if not g_NodeMgr:
        g_NodeMgr = CNodeMgr()
    return g_NodeMgr


class CNodeMgr(basemgr.CBaseMgr):
    def __init__(self):
        super(CNodeMgr, self).__init__()
        self.m_DefineInfo = {}  # 节点定义的信息

    # --------------定义节点的信息-----------------------
    def Register(self, sNodeName, oDefineNode):
        """注册定义的节点"""
        self.m_DefineInfo[sNodeName] = oDefineNode

    def GetAllDefineNodeName(self):
        return self.m_DefineInfo.keys()

    # ----------------编辑器节点信息-----------------------------
    def NewNode(self, bpID,  sNodeName, pos):
        """
        因为预定义节点和上面的pin是预先定义的，可以生成很多实例
        所以每创建一个节点，复制节点以及pin
        """
        oDefineNode = self.m_DefineInfo[sNodeName]
        oNode = copy.deepcopy(oDefineNode)
        nodeID = misc.uuid()
        GetIDMgr().SetNode2BP(bpID, nodeID)     # 记录node对应的bp
        GetBPMgr().AddNode2BP(nodeID)           # 添加到bp里面
        oNode.SetAttr(bddefine.NodeAttrName.ID, nodeID)
        oNode.SetAttr(bddefine.NodeAttrName.POSITION, pos)
        lstPin = []
        for _, oDefinePin in oNode.m_PinInfo.items():
            pinID = interface.AddPin(nodeID, oDefinePin)
            lstPin.append(pinID)
        oNode.SetAttr(bddefine.NodeAttrName.PINIDLIST, lstPin)
        self.m_ItemInfo[nodeID] = oNode
        return nodeID

    def DelNode(self, nodeID):
        oNode = self.m_ItemInfo.get(nodeID, None)
        if not oNode:
            return
        lstLine = interface.GetAllLineByNode(nodeID)
        for lineID in lstLine:
            interface.DelLine(lineID)
        lstPin = oNode.GetAttr(bddefine.NodeAttrName.PINIDLIST)
        for pinID in lstPin:
            interface.DelPin(pinID)
        del self.m_ItemInfo[nodeID]
        GetBPMgr().DelNode4BP(nodeID)
        bpID = GetIDMgr().DelNode2BP(nodeID)
        GetSignal().DEL_NODE.emit(bpID, nodeID)
