# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-04 21:22:41
@Desc: 各管理类的基类
"""


class CBaseMgr:
    def __init__(self):
        self.m_ItemInfo = {}
        self.m_ID = 0

    def NewID(self):
        self.m_ID += 1
        return self.m_ID

    def GetItem(self, key):
        return self.m_ItemInfo.get(key, None)

    def DelItem(self, key):
        if key in self.m_ItemInfo:
            oItem = self.m_ItemInfo[key]
            if hasattr(oItem, "Delete"):
                oItem.Delete()
            del self.m_ItemInfo[key]

    def SetItemAttr(self, ID, key, value):
        oLine = self.GetItem(ID)
        assert oLine is not None
        oLine.SetAttr(key, value)

    def GetItemAttr(self, ID, key):
        oLine = self.GetItem(ID)
        assert oLine is not None
        return oLine.GetAttr(key)

    def AddToAttrList(self, ID, sAttrName, value):
        oItem = self.GetItem(ID)
        if oItem:
            oItem.AppendToAttr(sAttrName, value)

    def DelFromAttrList(self, ID, sAttrName, value):
        oItem = self.GetItem(ID)
        if oItem:
            oItem.RemoveFromAttr(sAttrName, value)


class CBase:
    def __init__(self, *args):
        self.m_Info = {}

    def SetAttr(self, sAttrName, value):
        self.m_Info[sAttrName] = value

    def GetAttr(self, sAttrName):
        return self.m_Info[sAttrName]

    def AppendToAttr(self, sAttrName, value):
        lst = self.m_Info[sAttrName]
        if value not in lst:
            lst.append(value)

    def RemoveFromAttr(self, sAttrName, value):
        lst = self.m_Info[sAttrName]
        if value in lst:
            lst.remove(value)
