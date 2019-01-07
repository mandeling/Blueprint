# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-29 10:02:06
@Desc: 蓝图管理类
"""

import misc

from . import basemgr, interface
from . import define as eddefine
from .idmgr import GetIDMgr


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

    def GetItemSaveInfo(self, bpID):
        dTmp = super(CBPMgr, self).GetItemSaveInfo(bpID)
        dInfo = {
            eddefine.BP_ATTR_NAME_PREFIX: bpID
        }
        dInfo.update(dTmp)
        return dInfo

    def NewObj(self, ID):
        oItem = CBP(ID)
        return oItem


class CBP(basemgr.CBase):
    def __init__(self, ID, sName=None):
        super(CBP, self).__init__(ID)
        self.m_Info = {
            eddefine.BlueprintAttrName.ID: ID,
            eddefine.BlueprintAttrName.NAME: sName,
            eddefine.BlueprintAttrName.LINE_LIST: [],
            eddefine.BlueprintAttrName.NODE_LIST: [],
            eddefine.BlueprintAttrName.VARIABLE_LIST: [],
        }

    def GetSaveInfo(self):
        from .linemgr import GetLineMgr
        from .nodemgr import GetNodeMgr
        from .variablemgr import GetVariableMgr
        dSaveInfo = super(CBP, self).GetSaveInfo()
        lstLine = self.GetAttr(eddefine.BlueprintAttrName.LINE_LIST)
        for lineID in lstLine:
            dTmp = GetLineMgr().GetItemSaveInfo(lineID)
            dSaveInfo.update(dTmp)
        lstNode = self.GetAttr(eddefine.BlueprintAttrName.NODE_LIST)
        for nodeID in lstNode:
            dTmp = GetNodeMgr().GetItemSaveInfo(nodeID)
            dSaveInfo.update(dTmp)
        lstVariable = self.GetAttr(eddefine.BlueprintAttrName.VARIABLE_LIST)
        for varID in lstVariable:
            dTmp = GetVariableMgr().GetItemSaveInfo(varID)
            dSaveInfo.update(dTmp)
        return dSaveInfo

    def SetLoadInfo(self, dInfo):
        from .linemgr import GetLineMgr
        from .nodemgr import GetNodeMgr
        from .variablemgr import GetVariableMgr
        super(CBP, self).SetLoadInfo(dInfo)
        lstVariable = self.GetAttr(eddefine.BlueprintAttrName.VARIABLE_LIST)
        for varID in lstVariable:
            GetVariableMgr().LoadItemInfo(varID, dInfo)
            GetIDMgr().SetVar2BP(self.m_ID, varID)
        lstNode = self.GetAttr(eddefine.BlueprintAttrName.NODE_LIST)
        for nodeID in lstNode:
            GetNodeMgr().LoadItemInfo(nodeID, dInfo)
            GetIDMgr().SetNode2BP(self.m_ID, nodeID)
        lstLine = self.GetAttr(eddefine.BlueprintAttrName.LINE_LIST)
        for lineID in lstLine:
            GetLineMgr().LoadItemInfo(lineID, dInfo)
            GetIDMgr().SetLine2BP(self.m_ID, lineID)
