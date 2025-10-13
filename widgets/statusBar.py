from PyQt5.QtWidgets import QStatusBar, QLabel


class StatusBar(QStatusBar):
    def __init__(self, parent=None):
        QStatusBar.__init__(self, parent)
        self.parent = parent
        self.setup_status_bar()

    def setup_status_bar(self):
        status_label = QLabel("Препроцессор", parent=self.parent)
        self.addWidget(status_label)