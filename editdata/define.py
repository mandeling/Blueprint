# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-07 15:42:54
@Desc: 数据定义
"""


# ----------------------graphic-------------------------------
GRAPHIC_ATTR_NAME_PREFIX = "graphic_attr_name:"


class GraphicAttrName:
    ID = GRAPHIC_ATTR_NAME_PREFIX + "id"
    NAME = GRAPHIC_ATTR_NAME_PREFIX + "name"
    LINE_LIST = GRAPHIC_ATTR_NAME_PREFIX + "line_list"
    NODE_LIST = GRAPHIC_ATTR_NAME_PREFIX + "node_list"
    VARIABLE_LIST = GRAPHIC_ATTR_NAME_PREFIX + "variable_list"


# ----------------------Variable-------------------------------
VARIABLE_ATTR_NAME_PREFIX = "variable_attr_name:"
VARIABLE_TYPE_GLOBAL = 0
VARIABLE_TYPE_LOCAL = 1


class VariableAttrName:
    """变量属性名字的定义"""
    ID = VARIABLE_ATTR_NAME_PREFIX + "id"
    NAME = VARIABLE_ATTR_NAME_PREFIX + "name"
    TYPE = VARIABLE_ATTR_NAME_PREFIX + "type"
    VALUE = VARIABLE_ATTR_NAME_PREFIX + "value"



# ----------------------Line-------------------------------
LINE_ATTR_NAME_PREFIX = "line_attr_name:"


class LineAttrName:
    ID = LINE_ATTR_NAME_PREFIX + "id"
    OUTPUT_PINID = LINE_ATTR_NAME_PREFIX + "output_pin_id"
    INPUT_PINID = LINE_ATTR_NAME_PREFIX + "input_pin_id"
