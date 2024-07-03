import os

import hou

from .MsResource import MsMesh, MsTexture

class MsAsset():
    
    asset_type_map = {
        '3d': 'Ms3DAsset',
        '3dplant': 'Ms3DPlant',
        'surface': 'MsSurface' 
    }
    
    
    # From MS Documentation :
    # (https://docs.google.com/document/d/1ECABXde2UAq3gY9-YyxULa_of8tPnRzZQvPcG1LZt1A/edit)
    
    ms_dict_template = {
        "id":"",
        "name":"",
        "type":"",
        "resolution":"",
        "resolutionValue": 0,
        "path":"",
        "category":"",
        "textureFormat":"",
        "components":[],
        "meshList":[],
        "isCustom": False   
    }
            
    @staticmethod
    def fromData(asset_data: dict):
        
        type = asset_data.get('type')
        typeClass = MsAsset.asset_type_map.get(type)
        
        if typeClass != None:
            
            klass = globals().get(typeClass)
            
            return klass(asset_data)
        else:
            raise "Type not supported" #TODO: log error properly
    
    def __init__(self, asset_data):
        
        # Validate MS Asset:
        for key, value in self.ms_dict_template.items():
            if not type(asset_data.get(key)) == type(value):
                raise "MS Data not Valid" #TODO: log error properly
            
        
        # Name and ID
        self.name = hou.text.variableName(asset_data['name']).replace('_', '')
        self.id = hou.text.variableName(asset_data['id'])
        
        self.fullName = f"{self.name}_{self.id}"
        
        self.type = asset_data['type']
        
        
        # Tags
        tags: list[str] = asset_data['categories']
        if asset_data['tags'] != None: tags.extend(asset_data['tags'])
        
        self.tags = [hou.text.variableName(tag) for tag in tags ]
        
        
        self.msThumbnail = asset_data.get('previewImage')
        
        self._addExportSettings()
        
    @staticmethod
    def _addExportSettings():
        pass 
        
        
class MsTexturableAsset(MsAsset):
    def __init__(self, asset_data):
        super().__init__(asset_data)
        
        self.textures = []
        
        textures_data = asset_data['components'] + asset_data['components-billboard']
        
        for tex_data in textures_data:
            
            billboardLod = False
            if tex_data in asset_data['components-billboard']:
                billboardLod = True
            
            self.textures.append(
                MsTexture.fromTextureData(tex_data, billboardLod=billboardLod)
            )

    
    def getTexture(self, component, lod = None) -> MsTexture:
        for texture in self.textures:
            if texture.component == component:                
                if lod != None:
                    if texture.lod == lod:
                        return texture
                return texture
            
    def getOuputPath(self, texture):
        if texture.lod != None:
            name = f"{self.id}_{texture.component}_LOD{self.lod}.exr"
        
        else:
            name = f"{self.id}_{texture.component}.exr"
            
        return os.path.join(self.outputDir, 'textures', name)
    
    
    
class Ms3DAsset(MsTexturableAsset):
    def __init__(self, asset_data):
        super().__init__(asset_data)
        
        self.meshes = []
        
        for mesh_data in asset_data['lodList']:
            self.meshes.append(
                MsMesh.fromMeshData(mesh_data)
            )
        
        self.lods = [] 
        self.varCount = 0
        for mesh in self.meshes:
            if mesh.lod not in self.lods:
                self.lods.append(mesh.lod)
            
            self.varCount = max(self.varCount, mesh.var)
                
        self.lods.sort()      
        
        self.lodCount = len(self.lods)
        
        x, y ,z = 0.0, 0.0, 0.0
        for meta in asset_data['meta']:
            match meta['key']:
                case 'length':
                    x = float(meta['value'][:-1])
                    
                case 'width':
                    z = float(meta['value'][:-1])
                    
                case 'height':
                    y = float(meta['value'][:-1])
                    
        self.size = (x, y, z)
        
    def getMesh(self, var: int = 1, lod: int = 0) -> MsMesh:
        for mesh in self.meshes:
            if mesh.var == var and mesh.lod == lod:
                return mesh
        
        
class MsSurfaceAsset(MsTexturableAsset):
    def __init__(self, asset_data):
        super().__init__(asset_data)
        
        # TODO: Make it work for surface area !
        x, y ,z = 0.0, 0.0, 0.0
        for meta in asset_data['meta']:
            match meta['key']:
                case 'lenght':
                    x = float(meta['value'][:-1])
                    
                case 'width':
                    z = float(meta['value'][:-1])
                    
                case 'height':
                    y = float(meta['value'][:-1])
                        
        self.size = (x, y, z)

class Ms3DPlant(Ms3DAsset):
    def __init__(self, asset_data):
        super().__init__(asset_data)
