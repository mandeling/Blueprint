
import weakref
from . import slotui
from ui.BlueChartWidget import Ui_BlueChartWidget
from PyQt5.QtWidgets import QGraphicsProxyWidget, QGraphicsTextItem, QWidget
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QFont


class CBlueChartUI(QGraphicsProxyWidget):
    def __init__(self, oBlueChart, oScene, parent=None):
        super(CBlueChartUI, self).__init__(parent)
        self.m_BlueChart = weakref.ref(oBlueChart)
        self.m_Scene = weakref.ref(oScene)
        sName = oBlueChart.GetName()
        self.m_BlueChartWidget = Ui_BlueChartWidget()
        self.m_BlueChartWidgetParent = slotui.CWidget()
        self.m_BlueChartWidget.setupUi(self.m_BlueChartWidgetParent)
        self.m_BlueChartWidgetParent.GetStyle()
        self.m_BlueChartWidget.lb_Title.setText(sName)

        self.m_ChangeCharName = QGraphicsTextItem(self.m_BlueChartWidget.lb_Title.text(), self)
        self.m_ChangeCharName.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.m_ChangeCharName.setCursor(Qt.IBeamCursor)
        font = QFont()
        font.setPixelSize(18)
        self.m_ChangeCharName.setFont(font)
        self.m_ChangeCharName.setZValue(8)
        self.m_ChangeCharName.setParentItem(self)
        self.m_ChangeCharName.setPos(QPointF(self.m_BlueChartWidget.lb_Title.pos())+QPointF(10, 10))
        self.m_ChangeCharName.setTextWidth(self.m_BlueChartWidget.top.width())
        self.SetUnselectedWidget()
        self.setWidget(self.m_BlueChartWidgetParent)
        self.setZValue(4)


    def SetUnselectedWidget(self):
        self.m_BlueChartWidgetParent.SetStyle("Widget")
        self.setZValue(self.zValue()-10)
        self.m_ChangeCharName.hide()
        name = self.m_ChangeCharName.toPlainText()
        # TODO
        self.setSelected(False)


class CBlueChartWidget(Ui_BlueChartWidget, slotui.CWidget):
    def __init__(self, action, parent=None):
        super(CBlueChartWidget, self).__init__(parent)
        self.setupUi(self)
        self.m_Name = action.GetName()
        self.Init()
        self.InitSignal()
        self.show()

    def Init(self):
        self.lb_Title.setText(self.m_Name)
        self.btn_ShowProperty.setCursor(Qt.PointingHandCursor)
        self.btn_Source.hide()

    def InitSignal(self):
        self.btn_ShowProperty.clicked.connect(self.ShowProperty)

    def ShowProperty(self):
        pass
