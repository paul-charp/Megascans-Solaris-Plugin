from . import SocketListener
from . import SettingsManager
from . import Logger

from .UI.MainWindow import MSMainWindow


def initializePlugin():
    logger = Logger.getLogger("Debug")
    logger.setConsoleVerbosity(4)

    logger.fatal("Fatal")
    logger.error("Error")
    logger.warning("Warning")
    logger.importantMessage("ImportantMessage")
    logger.message("Message")
    logger.log("Just a log")

    # Get SettingsManager
    settings = SettingsManager.getInstance()
    # Init MainWindow
    mWindow = MSMainWindow.getInstance()
    mWindow.show()

    # Init SocketListener
    socketListener = SocketListener.getInstance()
    socketListener.start()
