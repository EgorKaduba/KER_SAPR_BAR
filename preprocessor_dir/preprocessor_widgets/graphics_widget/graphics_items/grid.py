from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPen


class GridItem(QGraphicsItem):
    def __init__(self, grid_size=20):
        super().__init__()
        self.grid_size = grid_size
        self.setFlag(QGraphicsItem.ItemDoesntPropagateOpacityToChildren)

    def boundingRect(self):
        return QRectF(-1000, -1000, 2000, 2000)

    def paint(self, painter, option, widget):

        pen = QPen(Qt.lightGray)
        pen.setWidth(0)
        painter.setPen(pen)

        left = -1000
        top = -1000
        right = 1000
        bottom = 1000

        x = left
        while x <= right:
            painter.drawLine(x, top, x, bottom)
            x += self.grid_size

        y = top
        while y <= bottom:
            painter.drawLine(left, y, right, y)
            y += self.grid_size