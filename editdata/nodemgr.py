# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-07 16:13:20
@Desc: 节点管理
"""

from .import define


class CNodeMgr:
    def __init__(self):
        self.m_Info = {}

    def NewBlueprint(self, bpID):
        self.m_Info[bpID] = CBpNodeMgr()

    def NewNode(self, bpID, sNodeName):
        oBpNode = self.m_Info[bpID]
        oBpNode.NewNode(sNodeName)


class CBpNodeMgr:
    def __init__(self):
        self.m_ID = 0
        self.m_Info = {}

    def NewID(self):
        self.m_ID += 1
        return self.m_ID

    def NewNode(self, sNodeName):
        uid = self.NewID()
        self.m_Info[uid] = CNode(uid, sNodeName)


class CNode:
    def __init__(self, uid, sNodeName):
        self.m_Info = {
            define.NodeAttrName.ID: uid,
            define.NodeAttrName.NAME: sNodeName,
            define.NodeAttrName.POSITION: (0, 0),
        }
