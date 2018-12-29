# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-29 10:19:16
@Desc: 保存各id直接的关系
"""

g_IDMgr = None


def GetIDMgr():
    global g_IDMgr
    if not g_IDMgr:
        g_IDMgr = CIDMgr()
    return g_IDMgr


class CIDMgr:
    def __init__(self):
        self.m_BPNodeInfo = {}
        self.m_Node2BP = {}

    def NewNode(self, bpID, nodeID):
        lst = self.m_BPNodeInfo.setdefault(bpID, [])
        if nodeID not in lst:
            lst.append(nodeID)
        self.m_Node2BP[nodeID] = bpID

    def DelNode(self, nodeID):
        bpID = self.m_Node2BP[nodeID]
        lst = self.m_BPNodeInfo.setdefault(bpID, [])
        if nodeID not in lst:
            lst.remove(nodeID)
        del self.m_Node2BP[nodeID]

    def GetBPIDByNodeID(self, nodeID):
        return self.m_Node2BP[nodeID]
