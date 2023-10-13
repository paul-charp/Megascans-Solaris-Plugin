from PySide2 import QtWidgets, QtCore, QtGui
import hou


class InputString(QtWidgets.QWidget):
    """docstring for InputString."""

    def __init__(self, label=None, value="", menu=None):
        super(InputString, self).__init__()
        self.label = label
        self.menu = menu
        self.value = value

        self.setupWidget()

    def setupWidget(self):
        self.layout = QtWidgets.QHBoxLayout()

        if self.label != None:
            self._label = QtWidgets.QLabel(self.label)
            self._label.setFixedWidth(90)
            self._label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            self._label.setStyleSheet("margin-right: 5px;")
            self._label.installEventFilter(self)
            self.layout.addWidget(self._label)

        self._inputField = QtWidgets.QLineEdit()
        self._inputField.setText(self.value)
        self._inputField.installEventFilter(self)
        self._inputField.editingFinished.connect(self.inputStyle)
        self.layout.addWidget(self._inputField)

        if self.menu != None:
            self._menu = QtWidgets.QPushButton()
            qmenu = QtWidgets.QMenu(self._menu)

            # for action in self.menu:
            qmenu.addAction("TEST")
            qmenu.addAction("TEST2")
            self._menu.setMenu(qmenu)
            self._menu.clicked.connect(self.debug_menu)
            self._menu.setProperty("menu", "true")
            self.layout.addWidget(self._menu)

        self.setLayout(self.layout)

    def debug_menu(self):
        print(self._menu.menu())

    def eventFilter(self, obj, event):
        if (
            self.layout.indexOf(obj) != -1
            and event.type() == QtCore.QEvent.MouseButtonRelease
        ):
            if (
                event.button() == QtCore.Qt.MiddleButton
                and event.modifiers() == QtCore.Qt.ControlModifier
            ):
                self._inputField.setText(self.value)

        return super(InputString, self).eventFilter(obj, event)

    def inputStyle(self):
        if self._inputField.text() == self.value:
            self._inputField.setStyleSheet("")

        else:
            self._inputField.setStyleSheet("font-weight: bold;")
