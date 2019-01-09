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
from .linemgr import GetLineMgr
from .nodemgr import GetNodeMgr

g_GraphicMgr = None


def GetGraphicMgr():
    global g_GraphicMgr
    if not g_GraphicMgr:
        g_GraphicMgr = CGraphicMgr()
    return g_GraphicMgr


class CGraphicMgr(basemgr.CBaseMgr):
    def NewGraphic(self, bpID):
        from .bpmgr import GetBPMgr
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
        }

    def Delete(self):
        from . import interface
        from .bpmgr import GetBPMgr
        lstLine = self.GetAttr(eddefine.GraphicAttrName.LINE_LIST)
        for lineID in lstLine:
            interface.DelLine(lineID)
        lstNode = self.GetAttr(eddefine.GraphicAttrName.NODE_LIST)
        for nodeID in lstNode:
            interface.DelNode(nodeID)
        GetBPMgr().DelGraphic4BP(self.m_ID)
        bpID = GetIDMgr().DelGraphic2BP(self.m_ID)

    def GetSaveInfo(self):
        dSaveInfo = super(CGraphic, self).GetSaveInfo()
        lstLine = self.GetAttr(eddefine.GraphicAttrName.LINE_LIST)
        for lineID in lstLine:
            dTmp = GetLineMgr().GetItemSaveInfo(lineID)
            dSaveInfo.update(dTmp)
        lstNode = self.GetAttr(eddefine.GraphicAttrName.NODE_LIST)
        for nodeID in lstNode:
            dTmp = GetNodeMgr().GetItemSaveInfo(nodeID)
            dSaveInfo.update(dTmp)
        return dSaveInfo

    def SetLoadInfo(self, dInfo):
        super(CGraphic, self).SetLoadInfo(dInfo)
        lstNode = self.GetAttr(eddefine.GraphicAttrName.NODE_LIST)
        for nodeID in lstNode:
            GetNodeMgr().LoadItemInfo(nodeID, dInfo)
            GetIDMgr().SetNode2Graphic(self.m_ID, nodeID)
        lstLine = self.GetAttr(eddefine.GraphicAttrName.LINE_LIST)
        for lineID in lstLine:
            GetLineMgr().LoadItemInfo(lineID, dInfo)
            GetIDMgr().SetLine2Graphic(self.m_ID, lineID)
