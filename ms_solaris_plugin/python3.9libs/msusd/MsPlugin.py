from .SocketListener import QLiveLinkMonitor
from .UI.MainWindow import MSMainWindow
from .Utils.jsondebug import tmp_json_write
from . import SettingsManager


def initializePlugin():
    # Get SettingsManager
    settings = SettingsManager.getInstance()

    # Init MainWindow
    mWindow = MSMainWindow.getInstance()
    mWindow.show()

    # Init SocketListener
    if len(QLiveLinkMonitor.Instance) == 0:
        bridge_monitor = QLiveLinkMonitor(settings.getSettings("socket_port"))
        bridge_monitor.Bridge_Call.connect(tmp_json_write)
        # bridge_monitor.start()
