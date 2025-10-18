# graphics_items.py
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsItem, QGraphicsTextItem
from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QBrush, QPen, QColor, QFont, QPainterPath

from preprocessor_dir.preprocessor_widgets.graphics_widget.graphics_items.concentrated_load import ConcentratedLoadItem
from preprocessor_dir.preprocessor_widgets.graphics_widget.graphics_items.distributed_load import DistributedLoadItem


class BarItem(QGraphicsRectItem):
    def __init__(self, bar_id, length, x_pos=0, parent=None):
        # Стержень будет представлен как тонкий прямоугольник
        super().__init__(0, -5, length, 10, parent)  # width=length, height=10
        self.bar_id = bar_id
        self.length = length
        self.x_pos = x_pos
        self.concentrated_loads = []
        self.distributed_loads = []
        self.setup_appearance()

    def setup_appearance(self):
        """Настройка внешнего вида стержня"""
        self.setPen(QPen(QColor(0, 0, 0), 2))  # Черная обводка
        self.setBrush(QBrush(QColor(200, 200, 255)))  # Светло-голубой фон
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, False)

        # Добавляем номер стержня
        self.id_text = QGraphicsTextItem(str(self.bar_id), self)
        self.id_text.setPos(self.length / 2 - 10, -25)
        self.id_text.setDefaultTextColor(QColor(0, 0, 0))

        # Добавляем линию стержня
        self.line_item = QGraphicsRectItem(0, -1, self.length, 2, self)
        self.line_item.setBrush(QBrush(QColor(0, 0, 0)))
        self.line_item.setPen(QPen(Qt.NoPen))

    def add_concentrated_load(self, node_number, force):
        """Добавить сосредоточенную нагрузку"""
        load = ConcentratedLoadItem(node_number, force, self)
        self.concentrated_loads.append(load)
        return load

    def add_distributed_load(self, node_number, force):
        """Добавить распределенную нагрузку"""
        load = DistributedLoadItem(node_number, force, self)
        self.distributed_loads.append(load)
        return load

    def update_loads(self, concentrated_data, distributed_data):
        """Обновить нагрузки на стержне"""
        # Очищаем старые нагрузки
        for load in self.concentrated_loads:
            self.scene().removeItem(load)
        for load in self.distributed_loads:
            self.scene().removeItem(load)

        self.concentrated_loads.clear()
        self.distributed_loads.clear()

        # Добавляем сосредоточенные нагрузки
        for load_data in concentrated_data:
            if load_data.get("node_number") in [self.bar_id, self.bar_id + 1]:
                self.add_concentrated_load(load_data["node_number"], load_data["power"])

        # Добавляем распределенные нагрузки
        for load_data in distributed_data:
            if load_data.get("node_number") == self.bar_id:
                self.add_distributed_load(load_data["node_number"], load_data["power"])

    def paint(self, painter, option, widget=None):
        """Кастомная отрисовка с выделением при выборе"""
        if self.isSelected():
            painter.setPen(QPen(QColor(255, 0, 0), 3))
        else:
            painter.setPen(QPen(QColor(0, 0, 0), 2))

        painter.setBrush(self.brush())
        painter.drawRect(self.rect())

