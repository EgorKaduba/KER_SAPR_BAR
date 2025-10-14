from PyQt5.QtWidgets import QDialog


class Manual(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("KER-SAPR-BAR Руководство пользователя")
        self.setModal(False)
        self.setFixedWidth(500)
        self.finished.connect(self.manual_close)

    def manual_close(self):
        self.parent.close_manual()
