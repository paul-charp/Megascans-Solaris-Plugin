from .SocketListener import QLiveLinkMonitor
from .UI.MainWindow import MSMainWindow
from .Utils.JsonOutput import tmp_json_write


def initializePlugin():
    # Init MainWindow
    mWindow = MSMainWindow.getInstance()
    mWindow.show()

    # Init SocketListener
    if len(QLiveLinkMonitor.Instance) == 0:
        bridge_monitor = QLiveLinkMonitor()
        bridge_monitor.Bridge_Call.connect(tmp_json_write)
        # bridge_monitor.start()
