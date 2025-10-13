from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QWidget


# class Graphics(QGraphicsView):
#     def __init__(self, parent=None):
#         QGraphicsView.__init__(self, parent)
#         self.setMinimumHeight(300)
#         self.scene = QGraphicsScene()
#         self.scene.setSceneRect(QRect(0, 0, 300, 300))
#         self.setScene(self.scene)

class Graphics(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setMinimumHeight(300)