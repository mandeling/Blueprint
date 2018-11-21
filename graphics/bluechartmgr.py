# -*- coding:utf-8 -*-
"""
@Author: xiaohao
@Date: 2018-11-21 14:48:12
@Desc: 节点数据管理对象
"""

import miscqt

g_BlueChartMgr = None


def GetBlueChartMgr():
    global g_BlueChartMgr
    if not g_BlueChartMgr:
        g_BlueChartMgr = CBlueChartMgr()
    return g_BlueChartMgr


class CBlueChartMgr:

    def __init__(self):
        super(CBlueChartMgr, self).__init__()
        self.m_ActionItem = {}
        self.m_SelectItem = []

    def NewChart(self, sName, tPos):
        idChart = miscqt.NewUuid()
        oAction = CBlueChart(idChart, sName, tPos)
        self.m_ActionItem[idChart] = oAction
        return idChart

    def GetChart(self, iID):
        if iID in self.m_ActionItem:
            return self.m_ActionItem[iID]
        return None

    def AddSelect(self, uid):
        if uid not in self.m_ActionItem:
            print("bm error", uid)
            return
        if uid not in self.m_SelectItem:
            self.m_SelectItem.append(uid)

    def ClearSelect(self):
        self.m_SelectItem = []


class CBlueChart:
    def __init__(self, id, sName, tPos):
        self.m_ID = id
        self.m_Name = sName
        self.m_Pos = tPos   # 相对于场景的位置

    def GetName(self):
        return self.m_Name

    def SetName(self, sName):
        self.m_Name = sName

    def GetID(self):
        return self.m_ID

    def GetPos(self):
        return self.m_Pos
