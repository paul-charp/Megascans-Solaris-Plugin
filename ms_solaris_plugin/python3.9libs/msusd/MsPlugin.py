from . import SocketListener
from .UI.MainWindow import MSMainWindow
from .Utils.jsondebug import tmp_json_write
from . import SettingsManager
from .Logger import Logger

import hou


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
