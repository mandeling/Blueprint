# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-17 11:31:20
@Desc: 蓝图ui的各种状态管理
"""

from . import uimgr


g_StatusMgr = None


def GetStatusMgr():
    global g_StatusMgr
    if not g_StatusMgr:
        g_StatusMgr = CStatusMgr()
    return g_StatusMgr


class CStatusMgr:
    def __init__(self):
        self.m_SelectNode = {}

    def GetSelectNode(self, bpID):
        return self.m_SelectNode.setdefault(bpID, [])

    def AddSelectNode(self, bpID, nodeID):
        """添加一个选中的节点"""
        lst = self.GetSelectNode(bpID)
        oNodeUI = uimgr.GetUIMgr().GetNodeUI(nodeID)
        if nodeID in lst:
            oNodeUI.SetUnpressStyle()
            lst.remove(nodeID)
        else:
            oNodeUI.SetPressStyle()
            lst.append(nodeID)

    def SelectOneNode(self, bpID, nodeID):
        """选中一个节点"""
        for nid in self.GetSelectNode(bpID):
            if nid == nodeID:
                continue
            oNodeUI = uimgr.GetUIMgr().GetNodeUI(nid)
            oNodeUI.SetUnpressStyle()
        self.m_SelectNode[bpID] = [nodeID]
        oNodeUI = uimgr.GetUIMgr().GetNodeUI(nodeID)
        oNodeUI.SetPressStyle()

    def ClearNode(self, bpID):
        """清除节点选中状态"""
        for nid in self.GetSelectNode(bpID):
            oNodeUI = uimgr.GetUIMgr().GetNodeUI(nid)
            oNodeUI.SetUnpressStyle()
        self.m_SelectNode[bpID] = []
