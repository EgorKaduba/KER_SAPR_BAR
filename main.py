from PyQt5.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QWidget, QLabel
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon

from widgets.menuBar import MenuBar
from widgets.statusBar import StatusBar

from preprocessor_dir.preprocessor import Preprocessor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_window_settings()
        self.menu_bar = MenuBar(parent=self)
        self.status_bar = StatusBar(parent=self)
        self.central_widget = QWidget()
        self.main_layout = QHBoxLayout()
        self.preprocessor = Preprocessor()
        self.setup_ui()
        self.file_path = None

    def setup_window_settings(self):
        self.setWindowTitle("KER-SAPR_BAR")
        icon = QIcon("images/icons/window_icon.png")
        self.setWindowIcon(icon)
        self.resize(QSize(1280, 720))

    def setup_ui(self):
        self.setMenuBar(self.menu_bar)
        self.setStatusBar(self.status_bar)

        self.main_layout.addWidget(self.preprocessor)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWinExtras import QtWin  # !!!

    myappid = 'mycompany.myproduct.subproduct.version'
    QtWin.setCurrentProcessExplicitAppUserModelID(myappid)  # noqa
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("images/icons/window_icon.png"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
