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
    def fromTextureData(tex_data):
            path        = os.path.normpath(tex_data['path'])
            component   = hou.text.variableName(tex_data['type'])
            
            match = re.search(MsTexture.lod_regex, path)
            if match != None:
                lod = int(match.group(1))
            else:
                lod = None
                
            return MsTexture(path, component, lod)
            
            
    
    def __init__(self, path: str, component: str, lod = None):       
        super(MsTexture, self).__init__(path)
        
        self.component = component
        
        self.colorspace = self.colorspace_map.get(
            self.ext
        )
        
        self.lod = lod
        
        
class MsMesh(MsResource):
    
    def __init__(self, path: str, var: int=1, lod: int=0):
        super(MsResource).__init__(path)

        self.var = var
        self.lod = lod
        
        
        
a = {
    "path": "\\\\lib.mtc.wtf\\librairie\\customMega\\Downloaded\\3d\\nature_rock_ukopeess\\ukopeess_4K_Normal_LOD0.jpg",
    "type": "normal",
    "resolution": "4K",
    "format": "jpg",
    "name": "ukopeess_4K_Normal_LOD0.jpg",
    "nameOverride": "Normal_4K_LOD0_ukopeess.jpg",
    "colorSpace": "Linear",
    "physicalSize": "1x1"
}

b = {
    "resolution": "4K",
    "type": "cavity",
    "path": "\\\\lib.mtc.wtf\\librairie\\customMega\\Downloaded\\3d\\nature_rock_ukopeess\\ukopeess_4K_Cavity.jpg",
    "format": "jpg",
    "name": "ukopeess_4K_Cavity.jpg",
    "nameOverride": "Cavity_4K__ukopeess.jpg",
    "colorSpace": "sRGB",
    "physicalSize": "1x1"
}

tex_a = MsTexture.fromTextureData(a)
tex_b = MsTexture.fromTextureData(b)

print(tex_a.lod)
print(tex_b.lod)