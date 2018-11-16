
import weakref
import miscqt

from PyQt5.QtWidgets import QGraphicsProxyWidget, QGraphicsTextItem, QGraphicsItem, QPushButton
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QPoint
from PyQt5.QtGui import QFont

from ui.BlueChartWidget import Ui_BlueChartWidget
from . import slotui
from .slotmgr import GetSlotMgr


class CBlueChartUI(QGraphicsProxyWidget):
    def __init__(self, oBlueChart, oScene, parent=None):
        super(CBlueChartUI, self).__init__(parent)
        self.m_BlueChart = weakref.ref(oBlueChart)
        self.m_Scene = weakref.ref(oScene)
        self.m_StartPos = None
        self.m_ChartIsMoving = False
        self.m_BlueChartWidget = Ui_BlueChartWidget()
        self.m_BlueChartWidgetParent = slotui.CWidget()
        self.m_ChangeCharName = None
        self.InitUI()
        self.InitSlot()
        self.InitSingle()

    def InitUI(self):
        self.m_BlueChartWidget.setupUi(self.m_BlueChartWidgetParent)
        self.m_BlueChartWidgetParent.GetStyle()
        sName = self.m_BlueChart().GetName()
        self.m_BlueChartWidget.lb_Title.setText(sName)

        self.m_ChangeCharName = CGraphicsTextItem(self.GetTitle(), self)
        self.m_ChangeCharName.setParentItem(self)
        self.m_ChangeCharName.setTextWidth(self.m_BlueChartWidget.top.width())

        self.SetUnselectedWidget()
        self.m_BlueChartWidget.btn_ShowProperty.setCursor(Qt.PointingHandCursor)
        # self.m_BlueChartWidget.btn_Source.hide()
        self.setWidget(self.m_BlueChartWidgetParent)
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.LeftButton)
        self.setFlags(
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemSendsGeometryChanges
        )
        self.setZValue(4)

    def InitSlot(self):
        """四个槽的初始化,先手动设置"""
        for oParent in (
            self.m_BlueChartWidget.btn_Input,
            self.m_BlueChartWidget.btn_Start,
            self.m_BlueChartWidget.btn_Source,
            self.m_BlueChartWidget.btn_End,
        ):
            qpos = oParent.mapToParent(QPoint(0, 0))
            pos = (qpos.x(), qpos.y())
            size = (oParent.width(), oParent.height())
            idSlot = miscqt.NewUuid()
            oSlot = GetSlotMgr().NewItem(idSlot, 1, self.m_BlueChart().GetID(), pos, size)
            oSlotUI = slotui.CSlotUI(idSlot, oSlot)
            oSlotUI.setParentItem(self)
            x, y = self.pos().x(), self.pos().y()
            x += oParent.x()
            y += oParent.y()
            mfsPos = oSlotUI.mapFromScene(x, y)
            mtpPos = oSlotUI.mapToParent(mfsPos)
            oSlotUI.setPos(mtpPos.x(), mtpPos.y())

            GetSlotMgr().AddView(idSlot, oSlotUI)

    def InitSingle(self):
        self.m_BlueChartWidget.btn_ShowProperty.clicked.connect(self.S_ShowProperty)
        self.m_ChangeCharName.SING_CHANGE_TITLE.connect(self.S_ChangeName)

    def SetUnselectedWidget(self):
        self.m_BlueChartWidgetParent.SetStyle("Widget")
        self.setZValue(self.zValue()-10)
        self.m_ChangeCharName.hide()
        name = self.m_ChangeCharName.toPlainText()
        # TODO
        self.setSelected(False)

    def mousePressEvent(self, event):
        super(CBlueChartUI, self).mousePressEvent(event)
        event.accept()
        if event.button() == Qt.LeftButton:
            self.m_StartPos = event.pos()
            self.m_ChartIsMoving = False

    def mouseMoveEvent(self, event):
        super(CBlueChartUI, self).mouseMoveEvent(event)
        self.SetMouseMovePos(self.m_StartPos, event.pos())

    def mouseReleaseEvent(self, event):
        super(CBlueChartUI, self).mouseReleaseEvent(event)
        if self.isSelected() and event.button() == Qt.LeftButton:
            pos = event.pos()
            rect = QRectF(self.m_BlueChartWidget.top.rect())
            rect.setWidth(rect.width() / 2)
            if rect.contains(pos):
                self.m_ChangeCharName.show()
                self.m_ChangeCharName.setPlainText(self.GetTitle())
                self.m_BlueChartWidget.lb_Title.hide()
        self.setSelected(True)

    def GetTitle(self):
        return self.m_BlueChartWidget.lb_Title.text()

    def SetMouseMovePos(self, sPos, ePos):
        if not (sPos and ePos):
            return
        pos = self.pos()
        x = pos.x() + ePos.x() - sPos.x()
        y = pos.y() + ePos.y() - sPos.y()
        self.setPos(x, y)

    def S_ShowProperty(self):
        import miscqt
        miscqt.NewUuid()
        pass

    def S_ChangeName(self, sTitle):
        sOldTitle = self.GetTitle()
        if sOldTitle != sTitle:
            self.m_BlueChartWidget.lb_Title.setText(sTitle)
            self.m_BlueChart().SetName(sTitle)
        self.m_BlueChartWidget.lb_Title.show()


class CGraphicsTextItem(QGraphicsTextItem):

    SING_CHANGE_TITLE = pyqtSignal(str)

    def __init__(self, sName, parent=None):
        super(CGraphicsTextItem, self).__init__(sName, parent)
        self.Init()

    def Init(self):
        self.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.setCursor(Qt.IBeamCursor)

        font = QFont()
        font.setPixelSize(18)
        self.setFont(font)
        self.setZValue(8)
        self.setPos(10, 10)

    def focusOutEvent(self, event):
        super(CGraphicsTextItem, self).focusOutEvent(event)
        sTitle = self.toPlainText()
        if sTitle:
            self.SING_CHANGE_TITLE.emit(sTitle)
        self.setPlainText("")
        self.hide()


QSS_STYLE = """
QWidget#BlueChartWidget{
    background:transparent;
}
QWidget#BCWidget{
    background:rgba(0, 0, 0, 200);
    border-style:solid;
    border-width:0px;
    border-radius:10px;
}
QWidget#top{
    border-style:solid;
    border-width:0px;
    background:qlineargradient(spread:pad, x1:0.00564972, y1:0.358, x2:1, y2:0.637, stop:0 rgba(0, 104, 183, 200), stop:1 rgba(0, 160, 233, 50));
    border-top-left-radius:10px;
    border-top-right-radius:10px;
    border-bottom-left-radius:0px;
    border-bottom-right-radius:0px;
}
QLabel{
    color:white;
}
QPushButton{
    background-color:transparent;
    color:white;
    border:none;
}
QPushButton:hover{
    background:qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(255, 0, 0, 0), stop:0.175141 rgba(255, 255, 255, 100), stop:0.824859 rgba(255, 255, 255, 100), stop:1 rgba(0, 0, 255, 0));
    border-image:transparent;
    color:white;
}
QWidget#outline{
    background:transparent;
    border:4px solid rgb(244, 100, 0);
    border-radius:14px;
}
"""


class CChartButtonUI(QPushButton):
    def __init__(self, parent=None):
        super(CChartButtonUI, self).__init__(parent)
        self.m_UID = miscqt.NewUuid()
