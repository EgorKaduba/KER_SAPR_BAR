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
        validator = None
        if self.column_type["type"] == "int":
            if self.column_type["plus"]:
                validator = QIntValidator(1, 1000000, parent)
            else:
                regex = QRegExp(r"^-?(0*[1-9]\d*)$")
                validator = QRegExpValidator(regex, parent)
        elif self.column_type["type"] == "float":
            if self.column_type["plus"]:
                regex = QRegExp(r"^(\d+\.?\d*|\.\d+)$")
            else:
                regex = QRegExp(r"^-?(\d*\.?\d*|\d+\.\d*)$")
            validator = QRegExpValidator(regex, parent)

        editor.setValidator(validator)
        return editor

    def setEditorData(self, editor, index):
        text = index.data(Qt.DisplayRole) or ""
        editor.setText(str(text))

    def setModelData(self, editor, model, index):
        text = editor.text().strip()

        if not text:
            text = self._get_default_value()
        else:
            text = self._validate_and_correct(text)

        model.setData(index, text, Qt.EditRole)

    def _get_default_value(self):
        if self.column_type["type"] == "int":
            return "1"
        else:
            return "1.0"

    def _validate_and_correct(self, text):
        if text in ["", ".", "-", "-."]:
            return self._get_default_value()

        try:
            if self.column_type["type"] == "int":
                value = int(text)
                if value == 0:
                    return self._get_default_value()
                if self.column_type["plus"] and value < 0:
                    return str(abs(value))
                return str(value)
            else:
                value = float(text)
                if value == 0:
                    return self._get_default_value()
                if self.column_type["plus"] and value < 0:
                    value = abs(value)
                if value == int(value):
                    return f"{int(value)}.0"
                else:
                    text = f"{value:.10f}".rstrip('0').rstrip('.')
                    if '.' not in text:
                        text += ".0"
                    if text == "0.0":
                        return self._get_default_value()
                    return text

        except ValueError:
            return self._get_default_value()