import json
import os
from PySide2.QtCore import Slot

import hou

from . import jsonutils
from ..Logger import Logger
from ..BatchUtils import parser


@Slot(str)
def tmp_json_write(jsondata):
    assets_data = json.loads(jsondata)

    for asset in assets_data:
        
        outData = parser.parseAssetData(asset)
        
        file = os.path.abspath(
            hou.text.expandString(
                f"$MSUSDPLUGIN/../.jsonoutput/{outData['fullName']}.json"))
        
        jsonutils.write_json(outData, file, indent=4, logger=Logger.getLogger("Dev"))
