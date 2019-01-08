# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-17 11:31:20
@Desc: 蓝图ui的各种状态管理
"""

from viewmgr.uimgr import GetUIMgr

g_StatusMgr = None


def GetStatusMgr():
    global g_StatusMgr
    if not g_StatusMgr:
        g_StatusMgr = CStatusMgr()
    return g_StatusMgr


class CStatusMgr:
    def __init__(self):
        self.m_SelectNode = {}  # 当前选择的节点
        self.m_CurGraphicID = None   # 当前选择的图标id

    def SetCurGraphicID(self, graphicID):
        self.m_CurGraphicID = graphicID

    def GetCurGraphicID(self):
        return self.m_CurGraphicID

    def GetSelectNode(self, graphicID):
        return self.m_SelectNode.setdefault(graphicID, [])

    def DelSelectNode(self, graphicID, nodeID):
        lst = self.GetSelectNode(graphicID)
        oNodeUI = GetUIMgr().GetNodeUI(nodeID)
        oNodeUI.SetUnpressStyle()
        if nodeID in lst:
            lst.remove(nodeID)

    def ChangeSelectNode(self, graphicID, nodeID):
        """添加一个选中的节点"""
        lst = self.GetSelectNode(graphicID)
        oNodeUI = GetUIMgr().GetNodeUI(nodeID)
        if nodeID in lst:
            oNodeUI.SetUnpressStyle()
            lst.remove(nodeID)
        else:
            oNodeUI.SetPressStyle()
            lst.append(nodeID)

    def SelectOneNode(self, graphicID, nodeID):
        """选中一个节点"""
        for nid in self.GetSelectNode(graphicID):
            if nid == nodeID:
                continue
            oNodeUI = GetUIMgr().GetNodeUI(nid)
            oNodeUI.SetUnpressStyle()
        self.m_SelectNode[graphicID] = [nodeID]
        oNodeUI = GetUIMgr().GetNodeUI(nodeID)
        oNodeUI.SetPressStyle()

    def ClearNode(self, graphicID):
        """清除节点选中状态"""
        for nid in self.GetSelectNode(graphicID):
            oNodeUI = GetUIMgr().GetNodeUI(nid)
            oNodeUI.SetUnpressStyle()
        self.m_SelectNode[graphicID] = []
