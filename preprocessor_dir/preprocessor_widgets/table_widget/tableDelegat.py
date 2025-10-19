from PyQt5.QtWidgets import QStyledItemDelegate, QLineEdit
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp


class TableDelegate(QStyledItemDelegate):
    def __init__(self, column_type: dict, parent=None):
        super().__init__(parent)
        self.column_type = column_type

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setAlignment(Qt.AlignHCenter)
        editor.setPlaceholderText("Любое число > 0")

        validator = None
        if self.column_type["type"] == "int":
            validator = QIntValidator()
            validator.setBottom(0 if self.column_type["plus"] else -1000000)
        elif self.column_type["type"] == "float":
            if self.column_type["plus"]:
                regex = QRegExp(r"^(\d+\.?\d*|\.\d+)$")
            else:
                regex = QRegExp(r"^-?(\d+\.?\d*|\.\d+)$")
            validator = QRegExpValidator(regex, parent)

        editor.setValidator(validator)
        return editor

    def setEditorData(self, editor, index):
        text = index.data(Qt.DisplayRole) or ""
        editor.setText(str(text))

    def setModelData(self, editor, model, index):
        text = editor.text()
        if self.column_type["type"] == "float" and text:
            text = self._ensure_positive_non_zero(text)

        model.setData(index, text, Qt.EditRole)

    def _ensure_positive_non_zero(self, text):
        """Обеспечивает, что число положительное и не равно 0"""
        text = text.strip()
        if text in ["", ".", "-", "-."]:
            return "1.0"
        try:
            value = float(text)
            if value <= 0:
                return "1.0"
            if text.endswith('.'):
                return text + "0"
            if text.startswith('.'):
                return "0" + text
            if text.startswith('-.'):
                return "0.1"
            if '.' not in text and text.replace('-', '').isdigit():
                return text + ".0"

            return text

        except ValueError:
            return "1.0"