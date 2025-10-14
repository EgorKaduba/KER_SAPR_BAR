from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSplitter
from PyQt5.QtCore import Qt

from preprocessor_dir.preprocessor_widgets.table_widget.table import Table
from preprocessor_dir.preprocessor_widgets.graphics import Graphics


class Preprocessor(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setStyleSheet("background-color: #d5dbe3;")
        self.main_layout = QHBoxLayout(self)
        self.splitter = QSplitter(Qt.Vertical)
        self.bar_table = Table("bar")
        self.concentrated_loads_table = Table("concentrated_loads")
        self.distributed_loads_table = Table("distributed_loads")
        self.graphics = Graphics()
        self.setup_ui()

    def setup_ui(self):
        self.splitter.addWidget(self.graphics)
        self.splitter.setChildrenCollapsible(False)

        tables_widget = QWidget()
        tables_layout = QHBoxLayout()
        tables_layout.addWidget(self.bar_table)
        tables_layout.addWidget(self.concentrated_loads_table)
        tables_layout.addWidget(self.distributed_loads_table)
        tables_layout.setContentsMargins(0, 0, 0, 0)
        tables_widget.setLayout(tables_layout)
        self.splitter.addWidget(tables_widget)

        self.splitter.setSizes([600, 300])
        self.main_layout.addWidget(self.splitter)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
