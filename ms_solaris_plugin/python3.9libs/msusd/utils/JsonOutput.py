import json
from PySide2.QtCore import Slot


@Slot(str)
def tmp_json_write(jsondata):
    assets_data = json.loads(jsondata)

    for asset in assets_data:
        print("Data Received", asset["id"])
        with open(f"{asset['id']}.json", "w") as json_file:
            json.dump(asset, json_file)
