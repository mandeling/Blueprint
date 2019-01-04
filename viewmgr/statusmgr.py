# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-17 11:31:20
@Desc: 蓝图ui的各种状态管理
"""

from viewmgr.uimgr import GetUIMgr
from editdata import interface

g_StatusMgr = None


def GetStatusMgr():
    global g_StatusMgr
    if not g_StatusMgr:
        g_StatusMgr = CStatusMgr()
    return g_StatusMgr


class CStatusMgr:
    def __init__(self):
        self.m_SelectNode = {}  # 当前选择的节点
        self.m_CurBPID = None   # 当前选择的蓝图id

    def SetCurBPID(self, bpID):
        self.m_CurBPID = bpID

    def GetCurBPID(self):
        return self.m_CurBPID

    def GetSelectNode(self, bpID):
        return self.m_SelectNode.setdefault(bpID, [])

    def DelSelectNode(self, bpID, nodeID):
        bpID = interface.GetBPIDByNodeID(nodeID)
        lst = self.GetSelectNode(bpID)
        oNodeUI = GetUIMgr().GetNodeUI(nodeID)
        oNodeUI.SetUnpressStyle()
        if nodeID in lst:
            lst.remove(nodeID)

    def ChangeSelectNode(self, bpID, nodeID):
        """添加一个选中的节点"""
        lst = self.GetSelectNode(bpID)
        oNodeUI = GetUIMgr().GetNodeUI(nodeID)
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
            oNodeUI = GetUIMgr().GetNodeUI(nid)
            oNodeUI.SetUnpressStyle()
        self.m_SelectNode[bpID] = [nodeID]
        oNodeUI = GetUIMgr().GetNodeUI(nodeID)
        oNodeUI.SetPressStyle()

    def ClearNode(self, bpID):
        """清除节点选中状态"""
        for nid in self.GetSelectNode(bpID):
            oNodeUI = GetUIMgr().GetNodeUI(nid)
            oNodeUI.SetUnpressStyle()
        self.m_SelectNode[bpID] = []
