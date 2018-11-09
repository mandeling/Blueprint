# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-11-09 09:56:09
@Desc: 

QGraphicsScene QGraphicsView QGraphicsItem三者之间的关系：
(1) QGraphicsScene是QGraphicsView中的场景：
    使用QGraphicsView::setScene()将scene加入到view中；
(2) QGraphicsScene又是QGraphicsItem的容器：
    使用QgraphicsScene::addItem()将item加入到scene中，或addRect()之类的添加图形函数，利用这些函数的返回值赋值给item即可达到相同效果；
"""

import sys
from PyQt5.QtWidgets import QApplication
from . import view


def Show():
    app = QApplication(sys.argv)
    obj = view.CBlueprintView()
    obj.show()
    sys.exit(app.exec_())
