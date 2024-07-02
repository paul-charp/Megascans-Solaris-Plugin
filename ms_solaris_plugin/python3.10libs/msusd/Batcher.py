from .MsObjects.MsAsset import MsAsset

import json
from PySide2.QtCore import Slot

from .Logger import Logger


@Slot(str)
def debugAssets(jsondata):
    assets_data = json.loads(jsondata)
    asset_list = {}
    for data in assets_data:
        asset = MsAsset.fromData(data)
        
        if asset.id not in asset_list:
            asset_list[asset.id] = asset
            
    # vis Debug
    for asset in asset_list.values():
        print(asset)
        print(asset.lods)
        print(asset.varCount)
        print(asset.meshes[0].path)
        print(asset.meshes[1].var)
        
        