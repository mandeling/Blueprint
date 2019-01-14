# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-04 21:22:41
@Desc: 各管理类的基类
"""

import copy


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
        oItem = self.GetItem(ID)
        assert oItem is not None
        oItem.SetAttr(key, value)

    def GetItemAttr(self, ID, key):
        oItem = self.GetItem(ID)
        assert oItem is not None
        return oItem.GetAttr(key)

    def AddToAttrList(self, ID, sAttrName, value):
        oItem = self.GetItem(ID)
        assert oItem is not None
        oItem.AppendToAttr(sAttrName, value)

    def DelFromAttrList(self, ID, sAttrName, value):
        oItem = self.GetItem(ID)
        assert oItem is not None
        oItem.RemoveFromAttr(sAttrName, value)

    def GetItemSaveInfo(self, ID):
        oItem = self.GetItem(ID)
        assert oItem is not None
        return oItem.GetSaveInfo()

    def NewObj(self, ID):
        raise Exception("子类未重载")

    def LoadItemInfo(self, ID, dInfo):
        obj = self.NewObj(ID)
        obj.SetLoadInfo(dInfo)
        self.m_ItemInfo[ID] = obj
        self.m_ID += 1


class CBase:
    def __init__(self, ID, *args):
        self.m_ID = ID
        self.m_Info = {}

    def GetID(self):
        return self.m_ID

    def GetInfo(self):
        return copy.deepcopy(self.m_Info)

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

    def SetLoadInfo(self, dInfo):
        dMyInfo = dInfo.pop(self.m_ID)
        self.m_Info = copy.deepcopy(dMyInfo)

    def GetSaveInfo(self):
        dSaveInfo = {self.m_ID: self.GetInfo()}
        return dSaveInfo
