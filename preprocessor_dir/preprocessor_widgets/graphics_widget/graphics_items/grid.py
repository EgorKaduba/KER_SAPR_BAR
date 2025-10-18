from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPen, QColor


class GridItem(QGraphicsItem):
    def __init__(self, grid_size=20):
        super().__init__()
        self.grid_size = grid_size
        self.setFlag(QGraphicsItem.ItemDoesntPropagateOpacityToChildren)

    def boundingRect(self):
        return QRectF(-10000, -10000, 20000, 20000)

    def paint(self, painter, option, widget):

        pen = QPen(QColor("#f5f3f0"))
        pen.setWidth(0)
        painter.setPen(pen)

        left = -10000
        top = -10000
        right = 10000
        bottom = 10000

        x = left
        while x <= right:
            painter.drawLine(x, top, x, bottom)
            x += self.grid_size

        y = top
        while y <= bottom:
            painter.drawLine(left, y, right, y)
            y += self.grid_size