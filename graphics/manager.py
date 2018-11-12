
import misc

from PyQt5.QtCore import pyqtSignal, QObject

@misc.Singleton
class CBlueChartMgr(QObject):
    SIG_ADD_CHART   = pyqtSignal(int)
    def __init__(self):
        QObject.__init__(self)
        # super(CBlueChartMgr, self).__init__()
        self.m_ActionItem = {}
        self.m_Index = 0
        print("----")

    def NewChart(self, sName, tPos):
        print(self, self.m_Index)
        self.m_Index += 1
        oAction = CBlueChart(self.m_Index, sName, tPos)
        self.m_ActionItem[self.m_Index] = oAction
        return self.m_Index


class CBlueChart:
    def __init__(self, id, sName, tPos):
        self.m_ID = id
        self.m_Name = sName
        self.m_Pos = tPos
