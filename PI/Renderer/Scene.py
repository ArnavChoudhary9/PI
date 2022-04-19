from typing import Iterable as _Iterable
from typing import Deque    as _Deque
from typing import List     as _List

from .Mesh import Mesh

from .Light import DirectionalLight, PointLight, SpotLight

import pyrr

class Scene:
    __Name   : str
    __Meshes : _Deque[Mesh]
    
    # Lights
    __DirectionalLight : DirectionalLight
    __PointLights      : _Deque[PointLight]
    __SpotLights       : _Deque[SpotLight]

    def __init__(self, name: str="DefaultScene") -> None:
        self.__Name   : str         = name
        self.__Meshes : _Deque[Mesh] = _Deque[Mesh]()

        self.__DirectionalLight : DirectionalLight   = DirectionalLight(pyrr.Vector3([ 0.0, -1.0, 0.0 ]))
        self.__PointLights      : _Deque[PointLight] = _Deque[PointLight]()
        self.__SpotLights       : _Deque[SpotLight]  = _Deque[SpotLight]()

    # Not yet Implemented
    # Serilization
    def Dump(self, filepath: str) -> None: raise NotImplementedError
    def Load(self, filepath: str) -> None: raise NotImplementedError

    # Mesh stuff
    @property
    def Meshes(self) -> _List[Mesh]:
        # return _List[Mesh](self.__Meshes)
        return self.__Meshes

    def AddMesh(self, mesh: Mesh):
        self.__Meshes.append(mesh)
        return self

    def AddMeshes(self, meshes: _Iterable[Mesh]):
        self.__Meshes.extend(meshes)
        return self

    def LoadMesh(self, path: str) -> _List[Mesh]:
        meshs = Mesh.Load(path)
        self.__Meshes.extend(meshs)
        return meshs

    # Light stuff
    @property
    def DirectionalLight(self) -> DirectionalLight:
        return self.__DirectionalLight

    def SetLightDirection(self, dir: pyrr.Vector3):
        self.__DirectionalLight.SetDirection(dir)
        return self

    @property
    def PointLights(self) -> _List[PointLight]:
        # return _List[PointLight](self.__PointLights)
        return self.__PointLights

    @property
    def PointLightLen(self) -> int:
        return min(len(self.__PointLights), 32)

    def _AddPointLight(self, light: PointLight):
        '''NOTE: Expects index to be set properly in range of [0, 32)
        '''

        self.__PointLights.append(light)
        return self

    def CreatePointLight(self,
        position : pyrr.Vector3=pyrr.Vector3([ 0.0, 0.0, 0.0 ]),
        diffuse  : pyrr.Vector3=pyrr.Vector3([ 0.8, 0.8, 0.8 ]),
        specular : pyrr.Vector3=pyrr.Vector3([ 0.8, 0.8, 0.8 ]),
        intensity: float = 1
        ):

        self._AddPointLight(PointLight(self.PointLightLen, position, diffuse, specular, intensity))
        return self

    @property
    def SpotLights(self) -> _List[SpotLight]:
        # return _List[SpotLight](self.__SpotLights)
        return self.__SpotLights

    @property
    def SpotLightLen(self) -> int:
        return min(len(self.__SpotLights), 32)

    def _AddSpotLight(self, light: SpotLight):
        '''NOTE: Expects index to be set properly in range of [0, 32)
        '''

        self.__SpotLights.append(light)
        return self

    def CreateSpotLight(self,
        position : pyrr.Vector3=pyrr.Vector3([ 0.0, 0.0, 0.0 ]),
        direction: pyrr.Vector3=pyrr.Vector3([ 0.0, -1.0, 0.0 ]),
        cutOff   : float=20,
        outerCutOff: float=25,
        diffuse  : pyrr.Vector3=pyrr.Vector3([ 0.8, 0.8, 0.8 ]),
        specular : pyrr.Vector3=pyrr.Vector3([ 0.8, 0.8, 0.8 ]),
        intensity: float = 1
        ):

        self._AddSpotLight(
            SpotLight(
                self.SpotLightLen,
                position, direction,
                cutOff, outerCutOff,
                diffuse, specular, intensity
            )
        )

        return self
