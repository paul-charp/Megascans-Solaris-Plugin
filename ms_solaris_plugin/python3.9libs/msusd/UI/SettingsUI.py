from PySide2.QtWidgets import (
    QVBoxLayout,
    QGroupBox,
    QGridLayout,
    QComboBox,
    QLabel,
    QCheckBox,
    QWidget,
    QFrame,
)
import hou
from .Widgets.DirChooser import QDirChooser


class SettingsUI(QWidget):
    def __init__(self):
        super(SettingsUI, self).__init__()
        self.setupSettingsUI()

    def setupSettingsUI(self):
        layout = QVBoxLayout()
        # debug = QLabel("test")
        export_path = QDirChooser("test", [], "")
        layout.addWidget(export_path)
        # layout.addWidget(debug)
        self.setLayout(layout)
