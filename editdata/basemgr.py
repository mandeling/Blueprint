# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-04 21:22:41
@Desc: 各管理类的基类
"""


class CBaseMgr:
    def __init__(self):
        self.m_ItemInfo = {}

    def GetItem(self, key):
        return self.m_ItemInfo.get(key, None)

    def DelItem(self, key):
        if key in self.m_ItemInfo:
            del self.m_ItemInfo[key]


class CBase:
    def __init__(self):
        self.m_Info = {}

    def SetAttr(self, sAttrName, value):
        self.m_Info[sAttrName] = value

    def GetAttr(self, sAttrName):
        return self.m_Info[sAttrName]
