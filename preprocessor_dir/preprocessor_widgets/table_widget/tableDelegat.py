from PyQt5.QtWidgets import QStyledItemDelegate, QLineEdit
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtCore import Qt


class TableDelegate(QStyledItemDelegate):
    def __init__(self, column_type: dict, parent=None):
        super().__init__(parent)
        self.column_type = column_type

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setAlignment(Qt.AlignHCenter)
        editor.setPlaceholderText("Введите число...")

        validator = None
        if self.column_type["type"] == "int":
            validator = QIntValidator()
            validator.setBottom(0 if self.column_type["plus"] else -1000000)
        elif self.column_type["type"] == "float":
            validator = QDoubleValidator()
            validator.setNotation(QDoubleValidator.StandardNotation)
            validator.setBottom(0 if self.column_type["plus"] else -1e6)
            validator.setTop(1e6)

        editor.setValidator(validator)
        return editor

    def setEditorData(self, editor, index):
        text = index.data(Qt.DisplayRole) or ""
        editor.setText(str(text))