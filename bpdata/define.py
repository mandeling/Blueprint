# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-07 17:10:02
@Desc:  蓝图定义
"""


PIN_INPUT_TYPE = 0
PIN_OUTPUT_TYPE = 1


class Type:
    INT = 1
    FLOAT = 2
    STR = 3


class NodeName:
    ADD = "加法节点"
    PRINT = "打印节点"


PIN_ATTR_NAME_PREFIX = "pin_attr_name:"


class PinAttrName:
    ID = PIN_ATTR_NAME_PREFIX + "id"
    NAME = PIN_ATTR_NAME_PREFIX + "name"
    PIN_TYPE = PIN_ATTR_NAME_PREFIX + "pin_type"
    DATA_TYPE = PIN_ATTR_NAME_PREFIX + "data_type"
