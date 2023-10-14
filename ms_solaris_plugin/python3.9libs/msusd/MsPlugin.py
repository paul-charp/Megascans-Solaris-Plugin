from . import SocketListener
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
    socketListener = SocketListener.getInstance()
    socketListener.start()
