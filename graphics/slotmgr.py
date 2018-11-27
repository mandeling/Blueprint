# -*- coding:utf-8 -*-
"""
@Author: xiaohao
@Date: 2018-11-21 14:51:56
@Desc: 信号槽全局数据管理对象
"""

from . import define

g_SlotMgr = None


def GetSlotMgr():
    global g_SlotMgr
    if not g_SlotMgr:
        g_SlotMgr = CSlotMgr()
    return g_SlotMgr


class CSlotMgr:
    def __init__(self):
        self.m_Items = {}
        self.m_SlotUIs = {}
        self.m_LastSelect = None  # 保存上一次选中的slotid

    def NewSlot(self, charID, pos, size, oBtn):
        idSlot = oBtn.GetUid()
        oSlot = CSlot(charID, pos, size, oBtn)
        self.m_Items[idSlot] = oSlot
        return oSlot

    def AddSlotUI(self, idSlot, oSlotUI):
        self.m_SlotUIs[idSlot] = oSlotUI

    def GetAllSlotUI(self):
        return self.m_SlotUIs

    def GetLastSelect(self):
        return self.m_LastSelect

    def SetLastSelect(self, uid):
        self.m_LastSelect = uid


class CSlot:
    def __init__(self, charID, pos, size, oBtn):
        self.m_UID = oBtn.GetUid()              # uuid
        self.m_SlotType = oBtn.GetSlotType()    # 类型 0-input 1-output
        self.m_VarType = oBtn.GetVarType()      # 变量类型
        self.m_CharID = charID                  # 父类的uuid
        self.m_Pos = pos                        # 相对于父类的pos坐标
        self.m_Size = size                      # (x, y)自身size
        self.m_Center = None
        self.SetCenter()

    def SetCenter(self):
        iOffset = 10    # 边距偏移
        if self.m_SlotType == define.INPUT_BTN_TYPE:
            self.m_Center = (0 - iOffset, self.m_Size[1]/2)
        else:
            self.m_Center = (self.m_Size[0] + iOffset, self.m_Size[1]/2)

    def GetCenter(self):
        return self.m_Center

    def GetPos(self):
        return self.m_Pos

    def GetSize(self):
        return self.m_Size

    def GetSlotType(self):
        return self.m_SlotType

    def GetChartID(self):
        return self.m_CharID

    def GetVarType(self):
        return self.m_VarType
