from PySide2.QtWidgets import QMainWindow, QVBoxLayout, QLineEdit, QWidget
from .SettingsUI import SettingsUI
import hou


class MSMainWindow(QMainWindow):
    __instance = None

    def __init__(self):
        if MSMainWindow.__instance != None:
            return
        else:
            super(MSMainWindow, self).__init__(hou.qt.mainWindow())
            MSMainWindow.__instance = self
            self.setWindowTitle("MS Solaris Plugin")
            self.setFixedWidth(600)
            self.setupMainWindow()

    def setupMainWindow(self):
        central_widget = QWidget()
        layout = QVBoxLayout()

        settingUI = SettingsUI()
        # batchUI = QLineEdit()

        layout.addWidget(settingUI)
        # layout.addWidget(batchUI)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        StyleSheet = """
"""

        self.setStyleSheet(StyleSheet)

    @staticmethod
    def getInstance():
        if MSMainWindow.__instance == None:
            MSMainWindow()
        return MSMainWindow.__instance
