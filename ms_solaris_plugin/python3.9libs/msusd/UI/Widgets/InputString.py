from PySide2 import QtWidgets, QtCore
import hou


class InputString(QtWidgets.QWidget):
    """
    Input String Custom Widget for Houdini
    Optionnal Menu and FileChooser

    """

    def __init__(self, label="Label", defaultValue="", menu=None, fileType=None):
        super(InputString, self).__init__()
        
        # Set Layout
        self.setLayout(QtWidgets.QHBoxLayout())
        
        # Add LineEdit
        self.defaultValue = defaultValue
        self.__initLineEdit()
        
        # Add Label
        if label != None:
            self.__initLabel(label)
            
        # Add Menu
        if menu != None:
            self.__initMenu(menu)
            
        # Add FileChooser
        if fileType != None:
            self.__initFileChooser(fileType)
        
    def __initLineEdit(self):
        self._lineEdit = QtWidgets.QLineEdit(self.defaultValue)
        
        self._lineEdit.installEventFilter(self)
        self._lineEdit.editingFinished.connect(self._updateLineEdit)
        
        self.layout().addWidget(self._lineEdit)
        
        return self._lineEdit
    
    def __initLabel(self, label):
        self._label = QtWidgets.QLabel(label)
        
        self._label.setFixedWidth(100)
        self._label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self._label.setStyleSheet("margin-right: 5px;")
        
        self._label.installEventFilter(self)
        
        self.layout().insertWidget(0, self._label)
        
        return self._label
    
    def __initMenu(self, menu):
        self._menu = QtWidgets.QPushButton()
        
        qMenu = QtWidgets.QMenu(self._menu)
        for action in menu:
            qAction = qMenu.addAction(action)
            qAction.triggered.connect(self._menuTriggered)
            
        self._menu.setMenu(qMenu)
        self._menu.setProperty("menu", "true")
        
        self.layout().addWidget(self._menu)
    
        return self._menu
    
    def __initFileChooser(self, fileType):
        self._fileChooser = hou.qt.FileChooserButton()
        self._fileChooser.setFileChooserStartDirectory(self._lineEdit.text())
        self._fileChooser.setFileChooserFilter(fileType)
        
        self._fileChooser.fileSelected.connect(self._fileSelected)
        
        self.layout().addWidget(self._fileChooser)

        return self._fileChooser
    
    def _updateLineEdit(self):
        if self._lineEdit.text() == self.defaultValue:
            self._lineEdit.setStyleSheet("")

        else:
            self._lineEdit.setStyleSheet("font-weight: bold;")
        
    def _fileSelected(self, path):
        self._lineEdit.setText(path)
        self._updateLineEdit()
        
    def _menuTriggered(self): 
        str = self.sender().text()
        self._lineEdit.setText(str)
        self._updateLineEdit()
        
    def eventFilter(self, obj, event):
        if (
            self.layout().indexOf(obj) != -1
            and event.type() == QtCore.QEvent.MouseButtonRelease
        ):
            if (
                event.button() == QtCore.Qt.MiddleButton
                and event.modifiers() == QtCore.Qt.ControlModifier
            ):
                self._lineEdit.setText(self.defaultValue)
                self._updateLineEdit()

        return super(InputString, self).eventFilter(obj, event)

    def value(self):
        return self._lineEdit.text()
