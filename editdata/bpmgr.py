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
        return oBP

    def AddGraphic2BP(self, graphicID):
        bpID = GetIDMgr().GetBPByGraphic(graphicID)
        self.AddToAttrList(bpID, eddefine.BlueprintAttrName.GRAPHIC_LIST, graphicID)

    def DelGraphic4BP(self, graphicID):
        bpID = GetIDMgr().GetBPByGraphic(graphicID)
        self.DelFromAttrList(bpID, eddefine.BlueprintAttrName.GRAPHIC_LIST, graphicID)

    def DelBP(self, bpID):
        from . import interface
        oBP = self.GetItem(bpID)
        if not oBP:
            return
        lstGraphic = oBP.GetAttr(eddefine.BlueprintAttrName.GRAPHIC_LIST)
        for graphicID in lstGraphic:
            interface.DelGraphic(graphicID)
        self.DelItem(bpID)

    def NewObj(self, ID):
        oItem = CBP(ID)
        return oItem


class CBP(basemgr.CBase):
    def __init__(self, ID):
        super(CBP, self).__init__(ID)
        self.m_Info = {
            eddefine.BlueprintAttrName.ID: ID,
            eddefine.BlueprintAttrName.GRAPHIC_LIST: [],
        }
