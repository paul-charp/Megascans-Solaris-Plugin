from PySide2 import QtWidgets, QtCore


class QAdvLineEdit(QtWidgets.QWidget):
    def __init__(self, label=None, value="", menu=None):
        super(QAdvLineEdit, self).__init__()
        self.label = label
        self.value = value
        self.menu = menu

        self.setupWidget()

    def setupWidget(self):
        layout = QtWidgets.QHBoxLayout()

        if self.label != None:
            label = QtWidgets.QLabel(self.label)
            label.setFixedWidth(125)
            label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            layout.addWidget(label)

        self.line_edit = QtWidgets.QLineEdit(self.value)

        layout.addWidget(self.line_edit)

        if self.menu != None:
            pass  # Add Menu

        layout.setSpacing(10)
        self.setLayout(layout)

    def text(self):
        return self.line_edit.text()
