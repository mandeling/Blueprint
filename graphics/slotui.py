from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt


class CWidget(QWidget):
    def __init__(self, parent=None):
        super(CWidget, self).__init__(parent)
        self.m_Stype = {}
        self.setCursor(Qt.SizeAllCursor)

    def mousePressEvent(self, event):
        event.accept()

    def GetStyle(self):
        style = self.styleSheet()
        self.m_Stype["Widget"] = ""
        self.m_Stype["Press"] = ""
        sWidgetStyle = "QWidget#outline{background:transparent;}"
        sWidgetPressStr = "QWidget#outline{"
        sWidgetPressStyle = ""
        iIndex = style.find(sWidgetPressStr)
        if iIndex != -1:
            tmpStyle = style[iIndex:]
            iEnd = tmpStyle.find("}") + 1
            sWidgetPressStyle = tmpStyle[:iEnd]
            style = style.replace(sWidgetPressStyle, "")
        self.m_Stype["Widget"] = style + sWidgetStyle
        self.m_Stype["Press"] = style + sWidgetPressStyle

    def SetStyle(self, state):
        self.setStyleSheet(self.m_Stype.get(state, ""))
