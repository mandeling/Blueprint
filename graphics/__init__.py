# -*- coding:utf-8 -*-
"""
@Author: xiaohao
@Date: 2018-11-09 09:56:09
@Desc:

QGraphicsScene QGraphicsView QGraphicsItem三者之间的关系：
(1) QGraphicsScene是QGraphicsView中的场景：
    使用QGraphicsView::setScene()将scene加入到view中；
(2) QGraphicsScene又是QGraphicsItem的容器：
    使用QgraphicsScene::addItem()将item加入到scene中，或addRect()之类的添加图形函数，利用这些函数的返回值赋值给item即可达到相同效果；

QGraphicsScene 称为图形场景。
QGraphicsView 称为图形窗口。
GraphicsView提供了一个界面，它既可以管理大数量的定制2D graphical items
QGraphicsScene 表示GraphicsView中的场景，它有以下职责： 为管理大量的items提供一个快速的接口。 传播事件到每个item。 管理item的状态

"""

import sys
from PyQt5.QtWidgets import QApplication
from . import view


def Show():
    app = QApplication(sys.argv)
    obj = view.CBlueprintView()
    obj.show()
    sys.exit(app.exec_())
