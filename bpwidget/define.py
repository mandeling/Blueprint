# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-08 14:23:33
@Desc: 蓝图窗口定义
"""

BP_ATTR_VARIABLE = "变量"
BP_ATTR_EVENT = "事件"
BP_ATTR_GRAPHIC = "图表"


class SearchMatch:
    CASW_SENSITIVELY = 1    # 区分大小写
    WHOLE_WORDS = 2         # 全字匹配
    REGULAR = 4             # 正则表达式匹配
