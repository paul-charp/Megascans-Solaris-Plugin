from PySide2 import QtWidgets
from .Widgets import InputString
from ..Utils import SettingsManager
import hou

class SettingsUI(QtWidgets.QWidget):
    def __init__(self):
        super(SettingsUI, self).__init__()

        self.widgets = {}
        self.setLayout(QtWidgets.QVBoxLayout())

        self.setupSettingsUI()

    def setupSettingsUI(self):
        self.addWidget(
            "export_path",
            InputString(label="Export Path",
                        defaultValue="$HIP/usd",
                        menu=['$HIP/usd', '$MSLIB/usd'],
                        fileType=hou.fileType.Directory),
        )

        self.addWidget("t_render_thumbs", QtWidgets.QCheckBox("Render Thumbnails"))
        self.addWidget(
            "thumbs_size",
            hou.qt.InputField(hou.qt.InputField.IntegerType, 1, label="Thumbnail Size"),
        )
        self.addWidget("thumbs_renderer", QtWidgets.QComboBox()).addItems(
            ["Karma", "OpenGL"]
        )
        self.addWidget("t_proxy", QtWidgets.QCheckBox("Lowest LOD as Proxy"))
        self.addWidget("t_guide", QtWidgets.QCheckBox("Lowest LOD as Sim Guide"))
        self.addWidget("t_asset_gallery", QtWidgets.QCheckBox("Add To Asset Gallery"))
        
        self.addWidget(
            "asset_gallery_path",
            InputString(label="Asset Gallery File",
                        defaultValue="$HIP/asset_gallery.db",
                        fileType=hou.fileType.Gallery),
        )
        self.addWidget("t_extra_classes", QtWidgets.QCheckBox("Add Extra Classes"))
        self.addWidget(
            "t_ref_on_stage", QtWidgets.QCheckBox("Reference Asset on Stage")
        )
        

    def getSettings(self):
        settings = {}

        for name, widget in self.widgets.items():
            if type(widget) == InputString:
                settings[name] = widget.value()

            if type(widget) == QtWidgets.QCheckBox:
                settings[name] = widget.isChecked()

            if type(widget) == QtWidgets.QComboBox:
                settings[name] = widget.currentText()

        return settings

    def saveSettings(self):
        settings = {"export_settings": self.getSettings()}
        SettingsManager.saveSettings(settings)

    def addWidget(self, name, widget):
        self.widgets[name] = widget
        self.layout().addWidget(self.widgets[name])

        return widget
