from PyQt5.QtWidgets import QTableWidget, QPushButton, QAbstractItemView
from PyQt5.QtCore import Qt

from preprocessor_dir.preprocessor_widgets.table_widget.tableDelegat import TableDelegate


class Table(QTableWidget):
    types = {
        "bar": {
            "HeaderLabels": ["Длина, L [м]", "Поперечное сечение, А [м²]", "Модуль упругости E, Па",
                             "Напряжение [σ], Па"],
            "ColumnsWidth": [100, 170, 155, 135]
        },
        "concentrated_loads": {
            "HeaderLabels": ["Номер узла", "Сила, F [H]"],
            "ColumnsWidth": [150, 160]
        },
        "distributed_loads": {
            "HeaderLabels": ["Номер узла", "Сила, q [H]"],
            "ColumnsWidth": [150 ,160]
        }
    }
    def __init__(self, table_type: str = "bar", parent=None):
        QTableWidget.__init__(self, parent)
        self.type = table_type
        self.setColumnCount(len(self.types[self.type]["HeaderLabels"]))
        self.setRowCount(0)
        self.setMinimumWidth(sum(self.types[self.type]["ColumnsWidth"]) + 20)
        self.setHorizontalHeaderLabels(self.types[self.type]["HeaderLabels"])
        self.setStyleSheet("background-color: white; color: black;")
        self.horizontalHeader().setStretchLastSection(True)
        self.setSelectionMode(QAbstractItemView.NoSelection) # noqa
        for column in range(self.columnCount()):
            self.setColumnWidth(column, int(self.types[self.type]["ColumnsWidth"][column]))
        self.add_button_row()
        self.set_delegate()

    def set_delegate(self):
        if self.type == "bar":
            self.setItemDelegate(TableDelegate(parent=self, column_type={"type": "float", "plus": True}))
        if self.type == "concentrated_loads":
            self.setItemDelegateForColumn(0, TableDelegate(parent=self, column_type={"type": "int", "plus": True}))
            self.setItemDelegateForColumn(1,
                                          TableDelegate(parent=self, column_type={"type": "float", "plus": False}))
        if self.type == "ddistributed_loads":
            self.setItemDelegateForColumn(0, TableDelegate(parent=self, column_type={"type": "int", "plus": True}))
            self.setItemDelegateForColumn(1,
                                          TableDelegate(parent=self, column_type={"type": "float", "plus": False}))


    def get_info(self):
        for row in range(self.rowCount() - 1):
            for column in range(self.columnCount()):
                print(row, column)

    def add_data_row(self):
        row = self.rowCount()
        self.insertRow(row)

    def add_button_row(self):
        row = self.rowCount()
        self.insertRow(row)

        add_btn = QPushButton()
        add_btn.setStyleSheet("border: none;")
        add_btn.setText("+")
        add_btn.clicked.connect(self.add_new_row) # noqa

        self.setCellWidget(row, 0, add_btn)

    def add_new_row(self):
        row = self.rowCount() - 1
        self.clearSpans()
        self.removeRow(row)
        self.add_data_row()
        self.add_button_row()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace or event.key() == Qt.Key_Delete:
            self.delete_current_row()
        else:
            super().keyPressEvent(event)

    def delete_current_row(self):
        row = self.currentRow()
        if (row >= 0) and (row < (self.rowCount() - 1)):
            self.removeRow(row)