from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QBrush


class Graphics(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent=parent)
        self.setBackgroundBrush(QBrush(Qt.white))
        self.scene = QGraphicsScene(QRectF(0, 0, 300, 300), parent=self)
        self.setScene(self.scene)
        self.setMinimumHeight(300)