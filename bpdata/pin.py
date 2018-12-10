# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-07 17:43:07
@Desc: 节点引脚
"""

import copy
from . import define


class CFlowPin:
    """节点的流引脚"""

    def __init__(self, ID, iPinType, sName):
        self.m_Info = {
            define.PinAttrName.ID: ID,
            define.PinAttrName.NAME: sName,
            define.PinAttrName.PIN_TYPE: iPinType,
        }

    def GetInfo(self):
        return copy.deepcopy(self.m_Info)


class CDataPin:
    """节点的数据引脚"""

    def __init__(self, ID, iPinType, iDataType, sName):
        self.m_Info = {
            define.PinAttrName.ID: ID,
            define.PinAttrName.NAME: sName,
            define.PinAttrName.PIN_TYPE: iPinType,
            define.PinAttrName.DATA_TYPE: iDataType,
        }

    def GetInfo(self):
        return copy.deepcopy(self.m_Info)
