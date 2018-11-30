# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-11-30 14:40:03
@Desc: 
"""

import os
import weakref
import json
from PyQt5 import QtCore

g_LayoutMgr = None

LAYOUT_JSON = "layout.json"


def InitLayoutMgr(oWindow):
    global g_LayoutMgr
    if not g_LayoutMgr:
        g_LayoutMgr = None


class CLayoutMgr(QtCore.QObject):
    m_SaveDir = "PersonConfig"
    m_JsonFile = "layout.json"

    def __init__(self, oWindow):
        super(CLayoutMgr, self).__init__()
        self.m_Window = weakref.ref(oWindow)
        self.m_SaveFile = None
        self.m_Data = None
        self.Init()

    def Init(self):
        if not os.path.exists(self.m_SaveDir):
            os.makedirs(self.m_SaveDir)
        self.m_SaveFile = os.path.join(self.m_SaveDir, self.m_JsonFile)

