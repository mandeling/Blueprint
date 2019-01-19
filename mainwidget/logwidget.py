# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-18 14:25:12
@Desc: 日志面板
"""

import logging

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, \
    QPlainTextEdit, QMenu, QAction
from PyQt5.QtGui import QIcon, QPixmap, QColor, QTextCursor, QTextCharFormat, QTextBlockFormat


LEVEL_NAME = {
    logging.ERROR: "错误",
    logging.WARN: "警告",
    logging.INFO: "消息",
    logging.DEBUG: "调试",
}


LEVEL_COLOR = {
    logging.ERROR: QColor("#FF0000"),
    logging.WARN: QColor("#FFE600"),
    logging.INFO: QColor("#FFFFFF"),
    logging.DEBUG: QColor("#8CC932"),
}


g_LogWidget = None


def GetLogWidget():
    global g_LogWidget
    if not g_LogWidget:
        g_LogWidget = CLogWidget()
    return g_LogWidget


class CLogWidget(QWidget):
    def __init__(self, parent=None):
        super(CLogWidget, self).__init__(parent)
        self.m_FilterBtn = None
        self.m_SearchLine = None
        self.m_LogTextEdit = None
        self.m_Menu = None
        self.m_LineID = 0
        self.m_LevelShow = {iLevel: True for iLevel in LEVEL_NAME}
        self.m_LevelInfo = {iLevel: [] for iLevel in LEVEL_NAME}
        self._InitUI()
        self._InitSignal()
        self._InitMenu()

    def _InitUI(self):
        vBox = QVBoxLayout(self)
        hBox = QHBoxLayout()
        self.m_FilterBtn = QPushButton("过滤器")
        hBox.addWidget(self.m_FilterBtn)

        self.m_SearchLine = QLineEdit(self)
        self.m_SearchLine.setClearButtonEnabled(True)
        self.m_SearchLine.setPlaceholderText("搜索日志")
        hBox.addWidget(self.m_SearchLine)

        self.m_LogTextEdit = QPlainTextEdit(self)
        self.m_LogTextEdit.setReadOnly(True)

        vBox.addLayout(hBox)
        vBox.addWidget(self.m_LogTextEdit)

    def _InitSignal(self):
        self.m_SearchLine.textChanged.connect(self.S_SearchTextChanged)

    def _InitMenu(self):
        self.m_Menu = QMenu()
        for iLevel, sMenu in LEVEL_NAME.items():
            action = QAction(sMenu, self.m_Menu)
            action.level = iLevel
            action.setCheckable(True)
            action.setChecked(True)
            self.m_Menu.addAction(action)
            action.triggered.connect(self.S_OnFilterLevel)
        self.m_FilterBtn.setMenu(self.m_Menu)

    def AddLog(self, iLevel, sMsg):
        # sMsg = sMsg.replace("\r", "").replace("\n", "")   # 看情况需不需要去掉换行
        fmt = QTextCharFormat()
        fmt.setForeground(LEVEL_COLOR[iLevel])
        self.m_LogTextEdit.mergeCurrentCharFormat(fmt)
        self.m_LogTextEdit.appendPlainText(sMsg)

        # 记录一下每个等级对应那些行
        myDoc = self.m_LogTextEdit.document()
        for iNum in range(self.m_LineID, myDoc.lineCount()):
            self.m_LevelInfo[iLevel].append(iNum)
        self.m_LineID = myDoc.lineCount()

    def AddLog3(self, iLevel, sMsg):
        """设置背景色"""
        self.m_LogTextEdit.appendPlainText(sMsg)
        myDoc = self.m_LogTextEdit.document()
        fmt = QTextBlockFormat()
        fmt.setBackground(LEVEL_COLOR[iLevel])
        for iNum in range(self.m_LineID, myDoc.lineCount()):
            oTextBlock = myDoc.findBlockByNumber(iNum)
            oCursor = QTextCursor(oTextBlock)
            oCursor.mergeBlockFormat(fmt)
        self.m_LineID = myDoc.lineCount()

    def S_OnFilterLevel(self):
        sender = self.sender()
        level = sender.level
        bChecked = sender.isChecked()
        self.m_LevelShow[level] = bChecked
        self._RefreshLevel(level, bChecked)

    def S_SearchTextChanged(self):
        for iLevel, bShow in self.m_LevelShow.items():
            if not bShow:
                continue
            self._RefreshLevel(iLevel, bShow)

    def _RefreshLevel(self, iLevel, bShow):
        txt = self.m_SearchLine.text()
        doc = self.m_LogTextEdit.document()
        for iLine in self.m_LevelInfo[iLevel]:
            blk = doc.findBlockByNumber(iLine)
            if not bShow:
                blk.setVisible(False)
                continue
            if not txt:
                blk.setVisible(True)
                continue
            sLine = blk.text()
            if sLine.find(txt) == -1:
                blk.setVisible(False)
            else:
                blk.setVisible(True)
        self.m_LogTextEdit.viewport().update()
        doc.adjustSize()
        self.m_LogTextEdit.update()
