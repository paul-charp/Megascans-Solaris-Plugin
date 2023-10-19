import json
from PySide2.QtCore import Slot

from . import jsonutils
from ..Logger import Logger


@Slot(str)
def tmp_json_write(jsondata):
    assets_data = json.loads(jsondata)

    for asset in assets_data:
        file = f"{asset['id']}.json"
        jsonutils.write_json(asset, file, indent=4, logger=Logger.getLogger("Dev"))
