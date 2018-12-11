# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-11 15:08:24
@Desc: 蓝图图形场景借口
"""

from . import uimgr


def DelLine(bpID, lineID):
    oView = uimgr.GetUIMgr().GetBPView(bpID)
    oView.m_Scene.DelConnect(lineID)
