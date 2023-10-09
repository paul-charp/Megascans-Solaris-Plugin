from PySide2.QtCore import QThread, Signal
import time, socket

class QLiveLinkMonitor(QThread):
    """
    Bridge Socket Listener.
    From MSLiveLink Official Plugin
    """
    
    Bridge_Call = Signal(str)
    Instance = []
    
    def __init__(self):
        super(QLiveLinkMonitor, self).__init__()
        QLiveLinkMonitor.Instance.append(self)
        
        self.total_data = b''
        self.buffersize = 4096*2
        self.host = 'localhost'
        self.socket_port = 24981 #To Link to settings
        
    def __del__(self):
        self.quit()
        self.wait()
        
    def stop(self):
        self.terminate()
        
    def run(self):
        
        time.sleep(0.025)
        
        try:
            socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_.bind((self.host, self.socket_port))
            
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
                        if data : self.total_data += data
                        else : break
                        
                    time.sleep(0.05)
                    self.Bridge_Call.emit(self.total_data.decode('ascii'))
                    time.sleep(0.05)
                    
        except Exception as e:
            print("Socket Listener Error :", e)
    