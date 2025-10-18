from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsScene


class BarItem(QGraphicsRectItem):
    def __init__(self, x_pos: int = 0, y_pos: int = 0, length: int = 0, height: int = 0, parent: QGraphicsScene = None):
        super().__init__(x_pos, y_pos, length, height, parent)
        self.length = length
        self.height = height
        self.scene = parent