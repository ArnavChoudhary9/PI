from ..Renderer.Shader  import Shader
from ..Renderer.Texture import Texture2D
from ..Renderer.Mesh    import Mesh

from ..Logging.logger import PI_CORE_ASSERT

from dataclasses import dataclass as Struct
from multipledispatch import dispatch
import pathlib
from typing import Any, Dict, List, Callable
from uuid import UUID, NAMESPACE_URL
from uuid import uuid3 as _UUIDGenerator

UUIDGenerator: Callable[[str], UUID] = lambda asset: _UUIDGenerator(NAMESPACE_URL, asset)

@Struct
class Asset:
    Type: int
    Path: str
    UUID: UUID
    Asset: Any

class AssetManager:
    class AssetType:
        ShaderAsset, Texture2DAsset, MeshAsset \
            = range(0, 3)

    __slots__ = ("__AssetMap", "__CurrentProjectLocation")

    __Instance = None

    def __init__(self) -> None:
        self.__AssetMap: Dict[UUID, Asset] = {}
        self.__CurrentProjectLocation: str = ""
        AssetManager.__Instance = self

    def _GetUUID(self, asset: Any) -> UUID: return UUIDGenerator(asset.Path)
    def SetCurrentProjectLocation(self, loc: str) -> None: self.__CurrentProjectLocation = loc

    @property
    def CurrentProjectLocation(self) -> pathlib.Path:
        return pathlib.Path(self.__CurrentProjectLocation)
    
    def GetAbsolutePath(self, path: str) -> str:
        if path.count("InternalAssets") != 0: return path
        else:
            _path = self.CurrentProjectLocation.joinpath(pathlib.Path(path))
            if _path.exists(): return str(_path)
            else: return path

    def GetRelativePath(self, path: str) -> str:
        if path.count("InternalAssets") != 0: return path
        path: pathlib.Path = pathlib.Path(path)
        path = path.relative_to(self.CurrentProjectLocation)
        return str(path)

    @staticmethod
    def GetInstance(): return AssetManager.__Instance

    def Add(self, assetType: int, asset: Any) -> None:
        if assetType >= 3: PI_CORE_ASSERT(False, "Invalid AssetType: {}", assetType)

        uuid = self._GetUUID(asset)
        self.__AssetMap[uuid] = Asset(
            assetType, asset.Path, uuid, asset
        )

    def Load(self, assetType: int, path: str, _index: int=0) -> UUID:
        if assetType >= 3: PI_CORE_ASSERT(False, "Invalid AssetType: {}", assetType)
        path = self.GetAbsolutePath(path)

        asset = None
        if assetType == AssetManager.AssetType.ShaderAsset:
            asset: Shader = Shader.Create(path)
            self.Add(assetType, asset)

        elif assetType == AssetManager.AssetType.Texture2DAsset:
            asset: Texture2D = Texture2D.Create(path)
            self.Add(assetType, asset)

        elif assetType == AssetManager.AssetType.MeshAsset:
            assets: List[Mesh] = Mesh.Load(path)
            asset = assets[_index]
            self.Add(assetType, asset)

        return self._GetUUID(asset)

    @dispatch(str)
    def Get(self, path: str) -> Any:
        return self.__AssetMap.get(UUIDGenerator(self.GetAbsolutePath(path)), None).Asset

    @dispatch(UUID)
    def Get(self, uuid: UUID) -> Any: return self.__AssetMap.get(uuid, None).Asset