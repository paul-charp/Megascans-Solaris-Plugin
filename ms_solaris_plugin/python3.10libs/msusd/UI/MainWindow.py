from PySide2.QtWidgets import QMainWindow, QVBoxLayout, QLineEdit, QWidget
from .SettingsUI import SettingsUI
from .BatchUI import BatchController, BatchModel, BatchView
import hou
from .. import SocketListener


class MSMainWindow(QMainWindow):
    __instance = None

    def __init__(self):
        if MSMainWindow.__instance != None:
            return
        else:
            super(MSMainWindow, self).__init__(hou.qt.mainWindow())
            MSMainWindow.__instance = self
            self.setWindowTitle("MS Solaris Plugin")
            self.setMinimumWidth(600)
            self.setupMainWindow()
            self.setStyleSheet(self.getStylesheet())

    def setupMainWindow(self):
        central_widget = QWidget()
        layout = QVBoxLayout()

        settingUI = SettingsUI()

        layout.addWidget(settingUI)

        self.model = BatchModel()
        self.view = BatchView()
        self.controller = BatchController(self.model, self.view)

        layout.addWidget(self.view)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    @staticmethod
    def getStylesheet():
        StyleSheet = """
QLineEdit {
    font-family: Source Code Pro;
    color: white;
}
     """
        return StyleSheet

    @staticmethod
    def getInstance():
        if MSMainWindow.__instance == None:
            MSMainWindow()
        return MSMainWindow.__instance

    def closeEvent(self, event):
        socketListener = SocketListener.getInstance()
        socketListener.quit()
