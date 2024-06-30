from . import SocketListener
from . import SettingsManager
from . import Logger

from .UI.MainWindow import MSMainWindow


def initializePlugin():
    # Get Logger
    logger = Logger.getLogger("Plugin")

    # Get SettingsManager
    settings = SettingsManager.getInstance()

    # Init MainWindow
    mWindow = MSMainWindow.getInstance()
    mWindow.show()

    # Init SocketListener
    socketListener = SocketListener.getInstance()
    socketListener.start()
