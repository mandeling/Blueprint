# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-08 19:19:05
@Desc: 蓝图管理类
"""
import misc

from . import basemgr
from . import define as eddefine
from .idmgr import GetIDMgr
from .variablemgr import GetVariableMgr
from .graphicmgr import GetGraphicMgr

g_BPMgr = None


def GetBPMgr():
    global g_BPMgr
    if not g_BPMgr:
        g_BPMgr = CBPMgr()
    return g_BPMgr


class CBPMgr(basemgr.CBaseMgr):
    def NewBP(self):
        bpID = misc.uuid()
        oBP = CBP(bpID)
        self.m_ItemInfo[bpID] = oBP
        return bpID

    def AddGraphic2BP(self, graphicID):
        bpID = GetIDMgr().GetBPByGraphic(graphicID)
        self.AddToAttrList(bpID, eddefine.BlueprintAttrName.GRAPHIC_LIST, graphicID)

    def DelGraphic4BP(self, graphicID):
        bpID = GetIDMgr().GetBPByGraphic(graphicID)
        self.DelFromAttrList(bpID, eddefine.BlueprintAttrName.GRAPHIC_LIST, graphicID)

    def NewObj(self, ID):
        oItem = CBP(ID)
        return oItem


class CBP(basemgr.CBase):
    def __init__(self, ID):
        super(CBP, self).__init__(ID)
        self.m_Info = {
            eddefine.BlueprintAttrName.ID: ID,
            eddefine.BlueprintAttrName.GRAPHIC_LIST: [],
            eddefine.BlueprintAttrName.VARIABLE_LIST: [],
            eddefine.BlueprintAttrName.EVENT_NODE: None,
        }

    def Delete(self):
        from . import interface
        lstVar = self.GetAttr(eddefine.BlueprintAttrName.VARIABLE_LIST)
        for varID in lstVar:
            interface.DelVariable(varID)
        lstGraphic = self.GetAttr(eddefine.BlueprintAttrName.GRAPHIC_LIST)
        for graphicID in lstGraphic:
            interface.DelGraphic(graphicID)

    def GetSaveInfo(self):
        dSaveInfo = super(CBP, self).GetSaveInfo()
        lstVar = self.GetAttr(eddefine.BlueprintAttrName.VARIABLE_LIST)
        for varID in lstVar:
            dTmp = GetVariableMgr().GetItemSaveInfo(varID)
            dSaveInfo.update(dTmp)
        lstGraphic = self.GetAttr(eddefine.BlueprintAttrName.GRAPHIC_LIST)
        for graphicID in lstGraphic:
            dTmp = GetGraphicMgr().GetItemSaveInfo(graphicID)
            dSaveInfo.update(dTmp)
        return dSaveInfo

    def SetLoadInfo(self, dInfo):
        super(CBP, self).SetLoadInfo(dInfo)
        lstVar = self.GetAttr(eddefine.BlueprintAttrName.VARIABLE_LIST)
        for varID in lstVar:
            GetVariableMgr().LoadItemInfo(varID, dInfo)
            GetIDMgr().SetVar2BP(self.m_ID, varID)
        lstGraphic = self.GetAttr(eddefine.BlueprintAttrName.GRAPHIC_LIST)
        for graphicID in lstGraphic:
            GetGraphicMgr().LoadItemInfo(graphicID, dInfo)
            GetIDMgr().SetGraphic2BP(self.m_ID, graphicID)
