# -*- coding:utf-8 -*-
"""
@Author: xiaohao
@Date: 2018-11-21 14:49:38
@Desc: 节点配表信息
"""

CHART_DATA = {
    "测试1": {
        "input": [
            {"type": 1, "name": "Input1"},
            {},
            {"type": 2, "name": "Input2"},
        ],
        "output": [
            {},
            {"type": 3, "name": "Output1"},
            {"type": 4, "name": "O2"},
        ],
    },
    "测试2": {
        "input": [
            {},
            {"type": 4, "name": "Input1"},
            {"type": 3, "name": "Input2"},
        ],
        "output": [
            {},
            {"type": 2, "name": "Output1"},
        ],
    },
    "测试3": {
        "input": [
            {"type": 3, "name": "Input1"},
            {"type": 2, "name": "Input2"},
        ],
        "output": [
            {"type": 3, "name": "Output1"},
            {"type": 1, "name": "Output2"},
            {},
            {"type": 4, "name": "Output3"},
        ],
    },
}
