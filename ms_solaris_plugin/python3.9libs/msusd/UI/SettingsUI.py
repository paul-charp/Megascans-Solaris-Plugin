from PySide2 import QtWidgets
from .Widgets.DirChooser import QDirChooser
from .Widgets.QAdvLineEdit import QAdvLineEdit


class SettingsUI(QtWidgets.QWidget):
    def __init__(self):
        super(SettingsUI, self).__init__()

        self.widgets = {}
        self.layout = QtWidgets.QVBoxLayout()

        self.setupSettingsUI()

    def setupSettingsUI(self):
        self.addWidget("export_path", QAdvLineEdit("Export Path", value="$HIP/usd"))
        self.addWidget("t_render_thumbs", QtWidgets.QCheckBox("Render Thumbnails"))
        self.addWidget("thumbs_size", QAdvLineEdit("Thumbnail Size", value="256"))
        self.addWidget("t_proxy", QtWidgets.QCheckBox("Lowest LOD as Proxy"))
        self.addWidget("t_guide", QtWidgets.QCheckBox("Lowest LOD as Sim Guide"))
        self.addWidget("t_asset_gallery", QtWidgets.QCheckBox("Add To Asset"))
        self.addWidget(
            "asset_gallery_path",
            QAdvLineEdit("Asset Gallery DB File", value="$HIP/usd/asset_gallery.db"),
        )
        self.addWidget("t_extra_classes", QtWidgets.QCheckBox("Add Extra Classes"))
        self.addWidget(
            "t_ref_on_stage", QtWidgets.QCheckBox("Reference Asset on Stage")
        )

        button_debug = QtWidgets.QPushButton("DEBUG")
        button_debug.clicked.connect(self.getSettings)
        self.layout.addWidget(button_debug)

        # layout.addWidget(debug)
        self.setLayout(self.layout)

    def getSettings(self):
        settings = {}

        for name, widget in self.widgets.items():
            if type(widget) == QAdvLineEdit:
                settings[name] = widget.text()

            if type(widget) == QtWidgets.QCheckBox:
                settings[name] = widget.isChecked()

        return settings

    def saveSettings(self):
        pass

    def addWidget(self, name, widget):
        self.widgets[name] = widget
        self.layout.addWidget(self.widgets[name])

        return widget
