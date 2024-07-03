from PySide2.QtCore import QThread, Signal
import time, socket

from .Logger import Logger
from . import SettingsManager
from .Utils.jsondebug import tmp_json_write
from .Batcher import debugAssets


class SocketListener(QThread):
    """
    Bridge Socket Listener.
    From MSLiveLink Official Plugin
    """

    Bridge_Call = Signal(str)
    __instance = None

    def __init__(self):
        if SocketListener.__instance != None:
            SocketListener.getInstance()

        SocketListener.__instance = self
        super(SocketListener, self).__init__()

        self.settings = SettingsManager.getInstance()
        self.logger = Logger.getLogger("SocketListener")

        self.total_data = b""
        self.buffersize = 4096 * 2
        self.host = "localhost"
        self.socket_port = self.settings.getSettings("socket_port")
        #self.Bridge_Call.connect(tmp_json_write)
        self.Bridge_Call.connect(debugAssets)

    def __del__(self):
        self.quit()
        self.wait()

    def stop(self):
        self.logger.message("Socket Listener Stopped")
        self.terminate()

    def run(self):
        time.sleep(0.025)

        try:
            socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_.bind((self.host, self.socket_port))
            self.logger.message(f"Starting SocketListener on port {self.socket_port}")

            while True:
                socket_.listen(5)
                client, adress = socket_.accept()

                data = ""
                data = client.recv(self.buffersize)

                if data != "":
                    self.total_data = b""
                    self.total_data += data

                    while True:
                        data = client.recv(self.buffersize)
                        if data:
                            self.total_data += data
                        else:
                            self.logger.message(f"Received {len(self.total_data)}bytes")
                            break

                    time.sleep(0.05)
                    self.Bridge_Call.emit(self.total_data.decode("ascii"))
                    time.sleep(0.05)

        except Exception as e:
            self.logger.warning(e)

    @staticmethod
    def getInstance():
        if SocketListener.__instance == None:
            SocketListener()
        return SocketListener.__instance
