# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-29 10:02:06
@Desc: 蓝图管理类
"""

import misc

from . import basemgr
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

    def AddNode2BP(self, bpID, nodeID):
        self.m_Node2BP[nodeID] = bpID
        self.AddToAttrList(bpID, eddefine.BlueprintAttrName.NODE_LIST, nodeID)

    def DelNode4BP(self, nodeID):
        bpID = self.m_Node2BP.pop(nodeID, None)
        self.DelFromAttrList(bpID, eddefine.BlueprintAttrName.NODE_LIST, nodeID)

    def GetBpIDByNodeID(self, nodeID):
        return self.m_Node2BP[nodeID]


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
