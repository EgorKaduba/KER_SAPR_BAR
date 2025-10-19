from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsScene
from PyQt5.QtGui import QColor, QBrush


class BarItem(QGraphicsRectItem):
    def __init__(self, x_pos: int = 0, y_pos: int = 0, length: int = 0, height: int = 0, parent: QGraphicsScene = None):
        super().__init__(x_pos, y_pos, length, height, parent)
        self.length = length
        self.height = height
        self.scene = parent
        self.real_length = length / 100.0
        self.real_height = height / 100.0
        self.setAcceptHoverEvents(True)
        self.modulus_elasticity = 0
        self.voltage = 0
        self.setBrush(QBrush(QColor(255, 255, 255)))
        self.setPen(QColor(0, 0, 0))

    def set_properties(self, real_length: float, real_height: float, modulus_elasticity: float, voltage: float):
        """Устанавливает свойства стержня для отображения в подсказке"""
        self.real_length = real_length
        self.real_height = real_height
        self.modulus_elasticity = modulus_elasticity if modulus_elasticity is not None else 1.0
        self.voltage = voltage if voltage is not None else 1.0

    def hoverEnterEvent(self, event):
        """Событие при наведении курсора"""
        self.setBrush(QBrush(QColor(180, 220, 255)))
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        """Событие при уходе курсора"""
        self.setBrush(QBrush(QColor(255, 255, 255)))
        super().hoverLeaveEvent(event)