# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-10 10:04:07
@Desc: 搜索窗口
"""

import re

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout,\
    QLineEdit, QPushButton, QFrame, QTreeView, QAbstractItemView
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QStandardItemModel

from signalmgr import GetSignal
from . import define


class CSearchWidget(QWidget):
    m_BorderStyleSheet = """
        border-color: #800000;
        border-width: 2px;
        border-style: solid;
    """

    m_StyleSheet = """
        color: #FFFFFF;
        background-color: #7092BE;
        border-style: solid;
    """

    def __init__(self, bpID, parent=None):
        super(CSearchWidget, self).__init__(parent)
        self.m_BPID = bpID
        self.m_Status = 0
        self.m_Search = None
        self.m_CaseSensitively = None
        self.m_WholeWords = None
        self.m_Regular = None
        self.m_Tree = None
        self._InitUI()
        self._InitSignal()

    def _InitUI(self):
        vBox = QVBoxLayout(self)
        hBox = QHBoxLayout(self)
        self.m_Search = QLineEdit(self)
        self.m_Search.setFocusPolicy(Qt.ClickFocus)
        self.m_Search.setClearButtonEnabled(True)
        hBox.addWidget(self.m_Search)

        # self.m_BtnMatch = QPushButton("全匹配", self)
        # self.m_BtnMatch.setMaximumSize(QSize(25, 25))
        # self.m_BtnMatch.setToolTip("点击切换全匹配/模糊匹配")

        self.m_CaseSensitively = QPushButton("Aa", self)
        self.m_CaseSensitively.setMaximumSize(QSize(25, 25))
        self.m_CaseSensitively.setToolTip("区分大小写")

        self.m_WholeWords = QPushButton("Ab", self)
        self.m_WholeWords.setMaximumSize(QSize(25, 25))
        self.m_WholeWords.setToolTip("全字匹配")

        self.m_Regular = QPushButton(".*", self)
        self.m_Regular.setMaximumSize(QSize(25, 25))
        self.m_Regular.setToolTip("使用正则表达式匹配")
        hBox.addWidget(self.m_CaseSensitively)
        hBox.addWidget(self.m_WholeWords)
        hBox.addWidget(self.m_Regular)
        vBox.addLayout(hBox)

        line = QFrame(self)
        line.setMinimumSize(QSize(0, 2))
        line.setMaximumSize(QSize(1234567, 2))
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        vBox.addWidget(line)

        self.m_Tree = CSearchWidget(self)
        self.m_Tree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        vBox.addWidget(self.m_Tree)
        self.setLayout(vBox)

    def _InitSignal(self):
        self.m_CaseSensitively.clicked.connect(self.S_ChangeCase)
        self.m_WholeWords.clicked.connect(self.S_WholeWords)
        self.m_Regular.clicked.connect(self.S_Regular)
        self.m_Search.returnPressed.connect(self.S_Search)
        GetSignal().UI_SHOW_BP_SEARCH.connect(self.S_ShowBPSearch)

    def S_ChangeCase(self):
        self.m_Status ^= define.SearchMatch.CASW_SENSITIVELY
        self._ChangeBtnStatus(self.m_CaseSensitively, self.m_Status & define.SearchMatch.CASW_SENSITIVELY)

    def S_WholeWords(self):
        self.m_Status ^= define.SearchMatch.WHOLE_WORDS
        self._ChangeBtnStatus(self.m_WholeWords, self.m_Status & define.SearchMatch.WHOLE_WORDS)

    def S_Regular(self):
        self.m_Status ^= define.SearchMatch.REGULAR
        self._ChangeBtnStatus(self.m_Regular, self.m_Status & define.SearchMatch.REGULAR)

    def _ChangeBtnStatus(self, oBtn, bSelect):
        if bSelect:
            oBtn.setStyleSheet(self.m_BorderStyleSheet)
        else:
            oBtn.setStyleSheet(self.m_StyleSheet)

    def S_ShowBPSearch(self, bpID):
        if bpID == self.m_BPID:
            self.show()

    def S_Search(self):
        sText = self.m_Search.text()
        if not sText:
            return
        flag = 0
        if not self.m_Status & define.SearchMatch.CASW_SENSITIVELY:  # 忽略大小写
            flag |= re.IGNORECASE
        if self.m_Status & define.SearchMatch.WHOLE_WORDS:
            sText = "^%s$" % sText
        if self.m_Status & define.SearchMatch.REGULAR:
            pattern = re.compile(sText, flag)
        else:
            pass


class CSearchTree(QTreeView):
    def __init__(self, parent=None):
        super(CSearchTree, self).__init__(parent)
        self._InitUI()
        self._InitSignal()

    def _InitUI(self):
        self.setHeaderHidden(True)
        self.setModel(QStandardItemModel(self))

    def _InitSignal(self):
        self.doubleClicked.connect(self.S_ShowNode)

    def S_ShowNode(self, item):
        print("shownode:", item)
