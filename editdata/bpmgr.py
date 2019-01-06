# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-29 10:02:06
@Desc: 蓝图管理类
"""

import misc

from . import basemgr, interface
from .idmgr import GetIDMgr
from . import define as eddefine

g_BPMgr = None


def GetBPMgr():
    global g_BPMgr
    if not g_BPMgr:
        g_BPMgr = CBPMgr()
    return g_BPMgr


class CBPMgr(basemgr.CBaseMgr):
    def __init__(self):
        super(CBPMgr, self).__init__()
        self.m_Node2BP = {}

    def NewItem(self):
        uid = misc.uuid()
        sName = "蓝图%s" % self.NewID()
        oBP = CBP(uid, sName)
        self.m_ItemInfo[uid] = oBP
        return uid

    def AddNode2BP(self, nodeID):
        bpID = GetIDMgr().GetBPByNode(nodeID)
        self.AddToAttrList(bpID, eddefine.BlueprintAttrName.NODE_LIST, nodeID)

    def DelNode4BP(self, nodeID):
        bpID = GetIDMgr().GetBPByNode(nodeID)
        self.DelFromAttrList(bpID, eddefine.BlueprintAttrName.NODE_LIST, nodeID)

    def AddLine2BP(self, lineID):
        bpID = GetIDMgr().GetBPByLine(lineID)
        self.AddToAttrList(bpID, eddefine.BlueprintAttrName.LINE_LIST, lineID)

    def DelLine4BP(self, lineID):
        bpID = GetIDMgr().GetBPByLine(lineID)
        self.DelFromAttrList(bpID, eddefine.BlueprintAttrName.LINE_LIST, lineID)

    def DelBP(self, bpID):
        oBP = self.m_ItemInfo.get(bpID, None)
        if not oBP:
            return
        lstVar = oBP.GetAttr(eddefine.BlueprintAttrName.VARIABLE_LIST)
        for varID in lstVar:
            interface.DelVariable(varID)
        lstLine = oBP.GetAttr(eddefine.BlueprintAttrName.LINE_LIST)
        for lineID in lstLine:
            interface.DelLine(lineID)
        lstNode = oBP.GetAttr(eddefine.BlueprintAttrName.NODE_LIST)
        for nodeID in lstNode:
            interface.DelNode(nodeID)
        self.DelItem(bpID)


class CBP(basemgr.CBase):
    def __init__(self, ID, sName):
        super(CBP, self).__init__()
        self.m_Info = {
            eddefine.BlueprintAttrName.ID: ID,
            eddefine.BlueprintAttrName.NAME: sName,
            eddefine.BlueprintAttrName.LINE_LIST: [],
            eddefine.BlueprintAttrName.NODE_LIST: [],
            eddefine.BlueprintAttrName.VARIABLE_LIST: [],
        }

    def Delete(self):
        pass  # TODO
