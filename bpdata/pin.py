# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-07 17:43:07
@Desc: 节点引脚
"""

import copy
from . import define


class CPin:
    def __init__(self, iPinType, iDataType, sName):
        self.m_Info = {
            define.PinAttrName.ID: 0,
            define.PinAttrName.NAME: sName,
            define.PinAttrName.DISPLAYNAME: sName,
            define.PinAttrName.PIN_TYPE: iPinType,
        }
        if iPinType in (define.PIN_INPUT_DATA_TYPE, define.PIN_OUTPUT_DATA_TYPE):
            self.m_Info[define.PinAttrName.DATA_TYPE] = iDataType
            self.m_Info[define.PinAttrName.VALUE] = define.GetDefauleValue(iDataType),

    def GetInfo(self):
        return copy.deepcopy(self.m_Info)

    def SetAttr(self, sAttrName, value):
        self.m_Info[sAttrName] = value

    def GetAttr(self, sAttrName):
        return self.m_Info[sAttrName]
