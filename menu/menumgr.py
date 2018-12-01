# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-11-30 14:08:31
@Desc: 
"""

from PyQt5 import QtWidgets, QtCore, QtGui
from . import menudefine

g_MenuMgr = None


def InitMgr(oWindow):
    global g_MenuMgr
    if not g_MenuMgr:
        g_MenuMgr = CMenuMgr()


def GetMenuMgr():
    global g_MenuMgr
    if not g_MenuMgr:
        g_MenuMgr = CMenuMgr()
    return g_MenuMgr


class CMenuMgr(QtCore.QObject):
    def __init__(self):
        super(CMenuMgr, self).__init__()
        self.m_RootNode = CAbstraceNode("MenuBar")
        self.m_RootNode.SetData(menudefine.MENU_QTCLASS_NAME, QtWidgets.QMenuBar)

    def AddMenu(self, dInfo):
        if menudefine.MENU_SEPARATOR_NAME in dInfo:
            self.AddSeparator(dInfo)
            return
        menuPath = dInfo[menudefine.MENU_NAME]
        iIndex = dInfo.get("Index", None)
        lInfo = menuPath.split("/")
        nIndex = 0
        curNode = self.m_RootNode
        while nIndex < len(lInfo):
            curName = lInfo[nIndex]
            childNode = curNode.Find(curName)
            if not childNode:
                if nIndex == len(lInfo) - 1:
                    childNode = curNode.AddChild(curName, iIndex)
                    childNode.m_Data = dInfo
                    childNode.SetData(menudefine.MENU_QTCLASS_NAME, QtWidgets.QAction)
                else:
                    childNode = curNode.AddChild(curName)
                    childNode.SetData(menudefine.MENU_QTCLASS_NAME, QtWidgets.QMenu)
            curNode = childNode
            nIndex += 1

    def AddSeparator(self, dInfo):
        menuPath = dInfo[menudefine.MENU_SEPARATOR_NAME]
        iIndex = dInfo.get("Index", None)
        lInfo = menuPath.split("/")
        nIndex = 0
        curNode = self.m_RootNode
        while nIndex < len(lInfo):
            curName = lInfo[nIndex]
            childNode = curNode.Find(curName)
            if not childNode:
                if nIndex == len(lInfo) - 1:
                    childNode = curNode.AddChild(curName, iIndex)
                    childNode.SetData(menudefine.MENU_QTCLASS_NAME, None)
                else:
                    childNode = curNode.AddChild(curName)
                    childNode.SetData(menudefine.MENU_QTCLASS_NAME, QtWidgets.QMenu)
            elif nIndex == len(lInfo) - 1:
                curNode = childNode
                childNode = curNode.AddChild(curName, iIndex)
                childNode.SetData(menudefine.MENU_QTCLASS_NAME, None)
            curNode = childNode
            nIndex += 1

    def BuildChildMenu(self, pNode=None, qParent=None):
        if not pNode:
            pNode = self.m_RootNode
        cls = pNode.GetData(menudefine.MENU_QTCLASS_NAME)
        if not cls and qParent:
            qParent.addSeparator()
            return
        qObj = cls(pNode.m_Name) if cls is not QtWidgets.QMenuBar else cls()
        if cls is QtWidgets.QMenu:
            qParent.addMenu(qObj)
        elif cls is QtWidgets.QAction:
            qParent.addAction(qObj)
            bChecked = pNode.GetData(menudefine.MENU_CHECKED_NAME)
            if bChecked:
                qObj.setCheckable(True)
                qObj.setChecked(bChecked)
            sShortCut = pNode.GetData(menudefine.MENU_SHORTCUT_NAME)
            if sShortCut:
                qObj.setShortcut(sShortCut)
            sIconPath = pNode.GetData(menudefine.MENU_ICON_NAME)
            if sIconPath:
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(sIconPath), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                qObj.setIcon(icon)
            sTips = pNode.GetData(menudefine.MENU_TIPS_NAME)
            if sTips:
                qObj.setStatusTip(sTips)
            func = pNode.GetData(menudefine.MENU_FUNCTION_NAME)
            if func:
                qObj.triggered.connect(func)
        pNode.m_QtObject = qObj
        pNode.m_ChildList.sort(key=lambda pChild: pChild.m_SublingIndex)
        for pChild in pNode.m_ChildList:
            self.BuildChildMenu(pChild, qObj)
        return qObj


class CAbstraceNode:
    def __init__(self, name):
        self.m_Name = name
        self.m_Data = {}
        self.m_QtObject = None
        self.m_SublingIndex = 9999
        self.m_ChildList = []

    def SetData(self, key, value):
        if key in self.m_Data:
            raise Exception("已存在key:%s" % key)
        self.m_Data[key] = value

    def GetData(self, key, default=None):
        return self.m_Data.get(key, default)

    def Find(self, sName):
        for oChild in self.m_ChildList:
            if oChild.m_Name == sName:
                return oChild
        return None

    def AddChild(self, sName, nIndex=None):
        lstName = [oChild.m_Name for oChild in self.m_ChildList]
        if sName and sName in lstName:
            return
        oChild = CAbstraceNode(sName)
        if nIndex is not None:
            oChild.m_SublingIndex = nIndex
        self.m_ChildList.append(oChild)
        return oChild
