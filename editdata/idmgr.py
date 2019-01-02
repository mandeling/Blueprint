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
        self.m_BPNodeInfo = {}  # {bpID:[nodeID,]}
        self.m_Node2BP = {}     # {nodeID:bpID}
        self.m_NodePinInfo = {}  # {nodeID:[pinID,]}
        self.m_Pin2Node = {}    # {pinID:nodeID}

    def DelPB(self, bpID):
        for nodeID in self.m_BPNodeInfo[bpID]:
            self.DelNode(nodeID)
        del self.m_BPNodeInfo[bpID]

    def NewNode(self, bpID, nodeID):
        lst = self.m_BPNodeInfo.setdefault(bpID, [])
        if nodeID not in lst:
            lst.append(nodeID)
        self.m_Node2BP[nodeID] = bpID

    def DelNode(self, nodeID):
        # 删除引脚槽
        for pinID in self.m_NodePinInfo[nodeID]:
            del self.m_Pin2Node[pinID]
        del self.m_NodePinInfo[nodeID]

        # 删除节点
        bpID = self.m_Node2BP[nodeID]
        lst = self.m_BPNodeInfo.setdefault(bpID, [])
        if nodeID not in lst:
            lst.remove(nodeID)
        del self.m_Node2BP[nodeID]

    def GetBPIDByNodeID(self, nodeID):
        return self.m_Node2BP[nodeID]

    def NewPin(self, nodeID, pinID):
        lst = self.m_NodePinInfo.setdefault(nodeID, [])
        if pinID not in lst:
            lst.append(pinID)
        self.m_Pin2Node[pinID] = nodeID
