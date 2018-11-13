
import misc

from PyQt5.QtCore import pyqtSignal, QObject

g_BlueChartMgr = None


def GetBlueChartMgr():
    global g_BlueChartMgr
    if not g_BlueChartMgr:
        g_BlueChartMgr = CBlueChartMgr()
    return g_BlueChartMgr


class CBlueChartMgr(QObject):
    SIG_ADD_CHART = pyqtSignal(int)

    def __init__(self):
        super(CBlueChartMgr, self).__init__()
        self.m_ActionItem = {}
        self.m_Index = 0
        print("----")

    def NewChart(self, sName, tPos):
        self.m_Index += 1
        oAction = CBlueChart(self.m_Index, sName, tPos)
        self.m_ActionItem[self.m_Index] = oAction
        return self.m_Index

    def GetChart(self, iID):
        if iID in self.m_ActionItem:
            return self.m_ActionItem[iID]
        return None


class CBlueChart:
    def __init__(self, id, sName, tPos):
        self.m_ID = id
        self.m_Name = sName
        self.m_Pos = tPos

    def GetName(self):
        return self.m_Name

    def GetID(self):
        return self.m_ID

    def GetPos(self):
        return self.m_Pos
