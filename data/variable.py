# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-01 16:32:54
@Desc: 
"""

import random
import copy

g_Variable = None


def GetVariable():
    global g_Variable
    if not g_Variable:
        g_Variable = CVariable()
    return g_Variable


class CVariable:
    def __init__(self):
        self.m_Data = {}
        self.InitTestData()

    def InitTestData(self):
        for i in range(10):
            sName = "Test%s" % i
            dInfo = {
                "type": random.randint(0, 9),
                "value": random.randint(-999999, 999999)
            }
            self.m_Data[sName] = dInfo

    def GetAllVarInfo(self):
        return copy.deepcopy(self.m_Data)
