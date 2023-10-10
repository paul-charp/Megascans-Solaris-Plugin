from PySide2 import QtWidgets
import hou


class QDirChooser(QtWidgets.QWidget):
    """docstring for QDirChooser."""

    def __init__(self, label, presets, defaultValue):
        super(QDirChooser, self).__init__()
        self.label = label
        self.presets = presets
        self.defaultValue = defaultValue

        self.setupWidget()

    def setupWidget(self):
        layout = QtWidgets.QHBoxLayout()

        # label = QLabel(self.label)
        label = QtWidgets.QLabel(self.label)
        line_edit = QtWidgets.QLineEdit(self.defaultValue)
        # preset_menu = QMenu()
        qmenu = QtWidgets.QMenu()
        qmenu.addAction("test")

        # button = hou.qt.MenuButton(qmenu)
        button = hou.qt.MenuButton(qmenu)
        qmenu.addAction("test")

        layout.addWidget(label)
        layout.addWidget(line_edit)
        layout.addWidget(button)

        self.setLayout(layout)
