
import weakref
from . import slotui
from ui.BlueChartWidget import Ui_BlueChartWidget
from PyQt5.QtWidgets import QGraphicsProxyWidget, QGraphicsTextItem, QGraphicsItem, QWidget
from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QFont


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
        self.InitSingle()

    def InitUI(self):
        self.m_BlueChartWidget.setupUi(self.m_BlueChartWidgetParent)
        self.m_BlueChartWidgetParent.GetStyle()
        sName = self.m_BlueChart().GetName()
        self.m_BlueChartWidget.lb_Title.setText(sName)
        self.m_ChangeCharName = QGraphicsTextItem(self.GetTitle(), self)
        self.m_ChangeCharName.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.m_ChangeCharName.setCursor(Qt.IBeamCursor)
        font = QFont()
        font.setPixelSize(18)
        self.m_ChangeCharName.setFont(font)
        self.m_ChangeCharName.setZValue(8)
        self.m_ChangeCharName.setParentItem(self)
        tt = self.m_BlueChartWidget.lb_Title.pos() + QPointF(10, 10)
        self.m_ChangeCharName.setPos(tt)
        self.m_ChangeCharName.setTextWidth(self.m_BlueChartWidget.top.width())
        self.SetUnselectedWidget()
        self.m_BlueChartWidget.btn_ShowProperty.setCursor(Qt.PointingHandCursor)
        self.m_BlueChartWidget.btn_Source.hide()
        self.setWidget(self.m_BlueChartWidgetParent)
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.LeftButton)
        self.setFlags(
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemSendsGeometryChanges
        )
        self.setZValue(4)

    def InitSingle(self):
        self.m_BlueChartWidget.btn_ShowProperty.clicked.connect(self.ShowProperty)

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
            print(rect)
            rect.setWidth(rect.width() / 2)
            if rect.contains(pos):
                print("1111111")
                self.m_ChangeCharName.show()
                self.m_ChangeCharName.setPlainText(self.GetTitle())
                self.m_BlueChartWidget.lb_Title.setText("")
            else:
                print("2222222")
                self.m_ChangeCharName.hide()
                sName = self.m_ChangeCharName.toPlainText()
                if sName != "":
                    self.m_BlueChart().SetName(sName)
                    self.m_ChangeCharName.setPlainText("")
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

    def ShowProperty(self):
        pass
