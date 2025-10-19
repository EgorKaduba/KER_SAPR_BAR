from PyQt5.QtWidgets import QTableWidget, QPushButton, QAbstractItemView, QTableWidgetItem
from PyQt5.QtCore import Qt

from preprocessor_dir.preprocessor_widgets.table_widget.tableDelegat import TableDelegate


class Table(QTableWidget):
    types = {
        "bar": {
            "HeaderLabels": ["Длина, L [м]", "Поперечное сечение, А [м²]", "Модуль упругости E, Па",
                             "Напряжение [σ], Па"],
            "ColumnsWidth": [100, 170, 155, 135],
            "HeaderLabelsInfo": ["length", "square", "modulus_elasticity", "voltage"]
        },
        "concentrated_loads": {
            "HeaderLabels": ["Номер узла", "Сила, F [H]"],
            "ColumnsWidth": [150, 160],
            "HeaderLabelsInfo": ["node_number", "power"]
        },
        "distributed_loads": {
            "HeaderLabels": ["Номер узла", "Сила, q [H]"],
            "ColumnsWidth": [150, 160],
            "HeaderLabelsInfo": ["node_number", "power"]
        }
    }

    def __init__(self, table_type: str = "bar", parent=None):
        QTableWidget.__init__(self, parent)
        self.parent = parent
        self.type = table_type
        self.suppress_item_changed = False
        self.setColumnCount(len(self.types[self.type]["HeaderLabels"]))
        self.setRowCount(0)
        self.setMinimumWidth(sum(self.types[self.type]["ColumnsWidth"]) + 20)
        self.setHorizontalHeaderLabels(self.types[self.type]["HeaderLabels"])
        self.setStyleSheet("background-color: white; color: black;")
        self.horizontalHeader().setStretchLastSection(True)
        self.setSelectionMode(QAbstractItemView.NoSelection)  # noqa
        self.itemChanged.connect(self.on_item_changed)
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
            self.verticalHeader().hide()
        if self.type == "distributed_loads":
            self.setItemDelegateForColumn(0, TableDelegate(parent=self, column_type={"type": "int", "plus": True}))
            self.setItemDelegateForColumn(1,
                                          TableDelegate(parent=self, column_type={"type": "float", "plus": False}))
            self.verticalHeader().hide()

    def get_info(self):
        if self.rowCount() - 1:
            data = {
                "type": self.type,
                "count": 0,
                "info": []
            }
            for row in range(self.rowCount() - 1):
                row_data = dict()
                row_is_empty = True

                for column in range(self.columnCount()):
                    item = self.item(row, column)
                    if item and item.text().strip():
                        text = item.text().strip()
                        try:
                            if "." in text:
                                num = float(text)
                            else:
                                num = int(text)
                            row_data[self.types[self.type]["HeaderLabelsInfo"][column]] = num
                            row_is_empty = False
                        except ValueError:
                            row_data[self.types[self.type]["HeaderLabelsInfo"][column]] = text
                            row_is_empty = False
                if not row_is_empty:
                    data["info"].append(row_data)
                    data["count"] += 1

            return data if data["count"] > 0 else None
        return None

    def filling_from_file(self, info: dict):
        row_count = info["count"]
        self.removeRow(self.rowCount() - 1)
        self.setRowCount(row_count)
        self.suppress_item_changed = True
        for row in range(row_count):
            if self.type == "bar":
                length = info["info"][row].get("length", 1)
                height = info["info"][row].get("square", 1)
                modulus_elasticity = info["info"][row].get("modulus_elasticity", 1)
                voltage = info["info"][row].get("voltage", 1)
                self.parent.graphics.scene.add_bar(length, height, modulus_elasticity, voltage)
            for column in range(self.columnCount()):
                if self.item(row, column) is None:
                    self.setItem(row, column, QTableWidgetItem())
                column_name = self.types[self.type]["HeaderLabelsInfo"][column]
                value = info["info"][row].get(column_name)
                if isinstance(value, float):
                    value_str = f"{value}".rstrip('0').rstrip('.')
                    if '.' not in value_str and 'e' not in value_str.lower():
                        value_str += ".0"
                elif isinstance(value, int):
                    value_str = str(value)
                else:
                    value_str = str(value) if value is not None else ""

                self.item(row, column).setText(value_str)
        self.add_button_row()
        self.suppress_item_changed = False
        if self.type == "concentrated_loads":
            self.parent.update_concentrated_loads_display()

    def add_data_row(self):
        row = self.rowCount()
        self.insertRow(row)
        self.suppress_item_changed = True
        for column in range(self.columnCount()):
            default_value = "1" if self.type != "bar" else "1.0"
            item = QTableWidgetItem(default_value)
            item.setTextAlignment(Qt.AlignCenter)
            self.setItem(row, column, item)
        if self.type == "bar":
            length_text = self.item(row, 0).text() if self.item(row, 0) else "1.0"
            height_text = self.item(row, 1).text() if self.item(row, 1) else "1.0"
            modulus_text = self.item(row, 2).text() if self.item(row, 2) and self.item(row, 2).text() else "1.0"
            voltage_text = self.item(row, 3).text() if self.item(row, 3) and self.item(row, 3).text() else "1.0"

            length = float(length_text)
            height = float(height_text)
            modulus_elasticity = float(modulus_text)
            voltage = float(voltage_text)

            self.parent.graphics.scene.add_bar(length, height, modulus_elasticity, voltage)
        self.suppress_item_changed = False

    def add_button_row(self):
        row = self.rowCount()
        self.insertRow(row)

        add_btn = QPushButton()
        add_btn.setStyleSheet("border: none;")
        add_btn.setText("+")
        add_btn.clicked.connect(self.add_new_row)  # noqa

        self.setCellWidget(row, 0, add_btn)

    def add_new_row(self):
        row = self.rowCount() - 1
        self.removeRow(row)
        self.add_data_row()
        self.add_button_row()
        if self.type == "concentrated_loads":
            if self.parent.graphics.scene.bars:
                self.parent.update_concentrated_loads_display()
        elif self.type == "bar":
            self.parent.refresh_all_loads()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace or event.key() == Qt.Key_Delete:
            self.delete_current_row()
        else:
            super().keyPressEvent(event)

    def delete_current_row(self):
        row = self.currentRow()
        if (row >= 0) and (row < (self.rowCount() - 1)):
            self.removeRow(row)
            if self.type == "bar":
                self.parent.graphics.scene.remove_bar(row)
                self.parent.update_loads_tables_after_bar_removal(row)
            elif self.type == "concentrated_loads":
                self.parent.update_concentrated_loads_display()

    def on_item_changed(self, item):
        if (item.row() == self.rowCount() - 1) or self.suppress_item_changed:
            return
        if self.type == "bar":
            length_text = self.item(item.row(), 0).text() if self.item(item.row(), 0) and self.item(item.row(),
                                                                                                    0).text() else "1.0"
            height_text = self.item(item.row(), 1).text() if self.item(item.row(), 1) and self.item(item.row(),
                                                                                                    1).text() else "1.0"
            modulus_text = self.item(item.row(), 2).text() if self.item(item.row(), 2) and self.item(item.row(),
                                                                                                     2).text() else "1.0"
            voltage_text = self.item(item.row(), 3).text() if self.item(item.row(), 3) and self.item(item.row(),
                                                                                                     3).text() else "1.0"

            try:
                length = float(length_text)
                height = float(height_text)
                modulus_elasticity = float(modulus_text)
                voltage = float(voltage_text)
            except ValueError:
                length = 1.0
                height = 1.0
                modulus_elasticity = 1.0
                voltage = 1.0

            self.parent.graphics.scene.resize_bar(
                bar_id=item.row(),
                new_length=length,
                new_height=height,
                modulus_elasticity=modulus_elasticity,
                voltage=voltage
            )
            self.parent.refresh_all_loads()
        elif self.type == "concentrated_loads":
            self.parent.update_concentrated_loads_display()