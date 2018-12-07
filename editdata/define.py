# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-07 15:42:54
@Desc: 数据定义
"""


# ----------------------Variable-------------------------------
VARIABLE_ATTR_NAME_PREFIX = "variable_attr_name:"
VARIABLE_TYPE_GLOBAL = 0
VARIABLE_TYPE_LOCAL = 1


class VariableAttrName:
    """变量属性名字的定义"""
    NAME = VARIABLE_ATTR_NAME_PREFIX + "name"
    TYPE = VARIABLE_ATTR_NAME_PREFIX + "type"
    VALUE = VARIABLE_ATTR_NAME_PREFIX + "value"


# ----------------------Node-------------------------------
NODE_ATTR_NAME_PREFIX = "node_attr_name:"


class NodeAttrName:
    ID = NODE_ATTR_NAME_PREFIX + "id"
    NAME = NODE_ATTR_NAME_PREFIX + "name"
    POSITION = NODE_ATTR_NAME_PREFIX + "postion"
    PININFO = NODE_ATTR_NAME_PREFIX + "pin_info"
