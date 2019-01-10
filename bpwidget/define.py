# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-08 14:23:33
@Desc: 蓝图窗口定义
"""

BP_ATTR_VARIABLE = "变量"
BP_ATTR_EVENT = "事件"
BP_ATTR_GRAPHIC = "图表"


FULL_MATCH = 0     # 全匹配
FUZZY_MATCH = 1    # 模糊匹配


class SearchTreeItemType:
    BP = 0
    GRAPHIC = 1
    NODE = 2
    PIN = 3
