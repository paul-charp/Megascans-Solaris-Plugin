from PySide2.QtCore import Slot
from .SocketListener import QLiveLinkMonitor
import json

@Slot(str)
def tmp_json_write(jsondata):
    assets_data = json.loads(jsondata)

    for asset in assets_data:
        print("Data Received", asset['id'])   
        with open(f"{asset['id']}.json", "w") as json_file:
            json.dump(asset, json_file)


def initializeWindow() -> int:
    print("Plugin Init")
    
    if len(QLiveLinkMonitor.Instance) == 0:
        bridge_monitor = QLiveLinkMonitor()
        bridge_monitor.Bridge_Call.connect(tmp_json_write)
        bridge_monitor.start()
        
