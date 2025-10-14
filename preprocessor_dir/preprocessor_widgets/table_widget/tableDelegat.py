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
        validator = None
        if self.column_type["type"] == "int":
            validator = QIntValidator()
        elif self.column_type["type"] == "float":
            validator = QDoubleValidator()
            validator.setNotation(QDoubleValidator.StandardNotation)

        if self.column_type["plus"]:
            validator.setBottom(0)

        editor.setValidator(validator)
        return editor