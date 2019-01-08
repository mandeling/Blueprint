# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-29 10:02:06
@Desc: 蓝图图表管理类
"""

import misc

from . import basemgr
from . import define as eddefine
from .idmgr import GetIDMgr
from .bpmgr import GetBPMgr

g_GraphicMgr = None


def GetGraphicMgr():
    global g_GraphicMgr
    if not g_GraphicMgr:
        g_GraphicMgr = CGraphicMgr()
    return g_GraphicMgr


class CGraphicMgr(basemgr.CBaseMgr):
    def NewGraphic(self, bpID):
        graphicID = misc.uuid()
        sName = "Graphic-%s" % self.NewID()
        oGraphic = CGraphic(graphicID, sName)
        GetIDMgr().SetGraphic2BP(bpID, graphicID)
        GetBPMgr().AddGraphic2BP(graphicID)
        self.m_ItemInfo[graphicID] = oGraphic
        return graphicID

    def AddNode2Graphic(self, nodeID):
        graphicID = GetIDMgr().GetGraphicByNode(nodeID)
        self.AddToAttrList(graphicID, eddefine.GraphicAttrName.NODE_LIST, nodeID)

    def DelNode4Graphic(self, nodeID):
        graphicID = GetIDMgr().GetGraphicByNode(nodeID)
        self.DelFromAttrList(graphicID, eddefine.GraphicAttrName.NODE_LIST, nodeID)

    def AddLine2Graphic(self, lineID):
        graphicID = GetIDMgr().GetGraphicByLine(lineID)
        self.AddToAttrList(graphicID, eddefine.GraphicAttrName.LINE_LIST, lineID)

    def DelLine4Graphic(self, lineID):
        graphicID = GetIDMgr().GetGraphicByLine(lineID)
        self.DelFromAttrList(graphicID, eddefine.GraphicAttrName.LINE_LIST, lineID)

    def DelGraphic(self, graphicID):
        from . import interface
        oGraphic = self.m_ItemInfo.get(graphicID, None)
        if not oGraphic:
            return
        lstVar = oGraphic.GetAttr(eddefine.GraphicAttrName.VARIABLE_LIST)
        for varID in lstVar:
            interface.DelVariable(varID)
        lstLine = oGraphic.GetAttr(eddefine.GraphicAttrName.LINE_LIST)
        for lineID in lstLine:
            interface.DelLine(lineID)
        lstNode = oGraphic.GetAttr(eddefine.GraphicAttrName.NODE_LIST)
        for nodeID in lstNode:
            interface.DelNode(nodeID)
        self.DelItem(graphicID)
        GetBPMgr().DelGraphic4BP(graphicID)
        bpID = GetIDMgr().DelGraphic2BP(graphicID)

    def NewObj(self, ID):
        oItem = CGraphic(ID)
        return oItem


class CGraphic(basemgr.CBase):
    def __init__(self, ID, sName=None):
        super(CGraphic, self).__init__(ID)
        self.m_Info = {
            eddefine.GraphicAttrName.ID: ID,
            eddefine.GraphicAttrName.NAME: sName,
            eddefine.GraphicAttrName.LINE_LIST: [],
            eddefine.GraphicAttrName.NODE_LIST: [],
            eddefine.GraphicAttrName.VARIABLE_LIST: [],
        }

    def GetSaveInfo(self):
        from .linemgr import GetLineMgr
        from .nodemgr import GetNodeMgr
        from .variablemgr import GetVariableMgr
        dSaveInfo = super(CGraphic, self).GetSaveInfo()
        lstLine = self.GetAttr(eddefine.GraphicAttrName.LINE_LIST)
        for lineID in lstLine:
            dTmp = GetLineMgr().GetItemSaveInfo(lineID)
            dSaveInfo.update(dTmp)
        lstNode = self.GetAttr(eddefine.GraphicAttrName.NODE_LIST)
        for nodeID in lstNode:
            dTmp = GetNodeMgr().GetItemSaveInfo(nodeID)
            dSaveInfo.update(dTmp)
        lstVariable = self.GetAttr(eddefine.GraphicAttrName.VARIABLE_LIST)
        for varID in lstVariable:
            dTmp = GetVariableMgr().GetItemSaveInfo(varID)
            dSaveInfo.update(dTmp)
        return dSaveInfo

    def SetLoadInfo(self, dInfo):
        from .linemgr import GetLineMgr
        from .nodemgr import GetNodeMgr
        from .variablemgr import GetVariableMgr
        super(CGraphic, self).SetLoadInfo(dInfo)
        lstVariable = self.GetAttr(eddefine.GraphicAttrName.VARIABLE_LIST)
        for varID in lstVariable:
            GetVariableMgr().LoadItemInfo(varID, dInfo)
            GetIDMgr().SetVar2Graphic(self.m_ID, varID)
        lstNode = self.GetAttr(eddefine.GraphicAttrName.NODE_LIST)
        for nodeID in lstNode:
            GetNodeMgr().LoadItemInfo(nodeID, dInfo)
            GetIDMgr().SetNode2Graphic(self.m_ID, nodeID)
        lstLine = self.GetAttr(eddefine.GraphicAttrName.LINE_LIST)
        for lineID in lstLine:
            GetLineMgr().LoadItemInfo(lineID, dInfo)
            GetIDMgr().SetLine2Graphic(self.m_ID, lineID)
