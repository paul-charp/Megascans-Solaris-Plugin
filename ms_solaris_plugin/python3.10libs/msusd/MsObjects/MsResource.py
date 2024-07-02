import os
import re

import hou


class MsResource(): 
    def __init__(self, path: str):

        self.path = os.path.normpath(path)
        self.ext  = os.path.splitext(self.path)
        
    def checkPath(self) -> bool:
        return os.path.isfile(self.path)
         
    
class MsTexture(MsResource):
    
    colorspace_map = {
        '.exr': 'linear',
        '.jpg': 'srgb'
    }
    
    lod_regex = r"_LOD(\d)"
    
    @staticmethod
    def fromTextureData(tex_data, billboardLod=False):
            path        = os.path.normpath(tex_data['path'])
            component   = hou.text.variableName(tex_data['type'])
            
            if billboardLod:
                lod = 'billboard'
                
            else:
                match = re.search(MsTexture.lod_regex, path)
                if match != None:
                    lod = int(match.group(1))
                else:
                    lod = None
                
            return MsTexture(path, component, lod)
            
            
    def __init__(self, path: str, component: str, lod = None):       
        super().__init__(path)
        
        self.component = component
        
        self.colorspace = self.colorspace_map.get(
            self.ext
        )
        
        self.lod = lod
        
        
class MsMesh(MsResource):
    
    @staticmethod
    def fromMeshData(mesh_data):
        path = os.path.normpath(mesh_data['path'])
        lod = mesh_data['lod']
        
        if lod != 'high':
            lod = lod[3:]
            
        var = mesh_data.get('variation')
        if var == None: var = 0
        
        return MsMesh(path, var, lod)
    
    def __init__(self, path: str, var: int=1, lod = 0):
        super().__init__(path)

        self.var = var
        self.lod = lod
    
        