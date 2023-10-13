from PySide2 import QtWidgets


class CWidgetBase(QtWidgets.QWidget):
    """docstring for CWidgetBase."""

    def __init__(self):
        super(CWidgetBase, self).__init__()

    @property
    def value(self):
        pass

    def createWidget(self, parent):
        pass
