
import miscqt

g_SlotMgr = None


def GetSlotMgr():
    global g_SlotMgr
    if not g_SlotMgr:
        g_SlotMgr = CSlotMgr()
    return g_SlotMgr


class CSlotMgr:
    def __init__(self):
        self.m_Items = {}
        self.m_Views = {}
        self.m_LastSelect = None  # 保存上一次选中的slotid

    def NewItem(self, idSlot, iType, charID, pos, size):
        oSlot = CSlot(idSlot, iType, charID, pos, size)
        self.m_Items[idSlot] = oSlot
        return oSlot

    def AddView(self, idSlot, oSlotUI):
        self.m_Views[idSlot] = oSlotUI

    def GetLastSelect(self):
        return self.m_LastSelect

    def SetLastSelect(self, uid):
        self.m_LastSelect = uid


class CSlot:
    def __init__(self, sUID, iType, charID, pos, size):
        self.m_UID = sUID       # uuid
        self.m_Type = iType     # 类型
        self.m_CharID = charID  # 父类的uuid
        self.m_Pos = pos        # 相对于父类的pos坐标
        self.m_Size = size
        self.m_Center = None
        self.SetCenter()

    def SetCenter(self):
        self.m_Center = (self.m_Size[0], self.m_Size[1])

    def GetCenter(self):
        return self.m_Center

    def GetPos(self):
        return self.m_Pos

    def GetSize(self):
        return self.m_Size