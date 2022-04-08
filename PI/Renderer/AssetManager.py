from typing import Any, Dict, List
from .Shader  import Shader
from .Texture import Texture2D
from .Mesh    import Mesh

from ..logger import PI_CORE_ASSERT

class AssetManager:
    class AssetType:
        ShaderAsset, Texture2DAsset, MeshAsset = range(0, 3)

    __slots__ = "__ShaderMap", "__Texture2DMap", "__MeshMap"

    def __init__(self) -> None:
        self.__ShaderMap    : Dict[str, Shader    ] = {}
        self.__Texture2DMap : Dict[str, Texture2D ] = {}
        self.__MeshMap      : Dict[str, Mesh      ] = {}

    def Add(self, assetType: int, asset) -> None:
        if assetType == AssetManager.AssetType.ShaderAsset:
            PI_CORE_ASSERT(self.__ShaderMap.get(asset, True), "Asset already added. Asset: <Shader>: {}", asset)
            self.__ShaderMap[asset.Name] = asset

        elif assetType == AssetManager.AssetType.Texture2DAsset:
            PI_CORE_ASSERT(self.__Texture2DMap.get(asset, True), "Asset already added. Asset: <Texture2D>: {}", asset)
            self.__Texture2DMap[asset.Name] = asset

        elif assetType == AssetManager.AssetType.MeshAsset:
            PI_CORE_ASSERT(self.__MeshMap.get(asset, True), "Asset already added. Asset: <Mesh>: {}", asset)
            self.__MeshMap[asset.Name] = asset

        else:
            PI_CORE_ASSERT(False, "Invalid AssetType: {}", assetType)

    def Load(self, assetType: int, path: str) -> Any:
        asset = None

        if assetType == AssetManager.AssetType.ShaderAsset:
            asset: Shader = Shader.Create(path)
            self.Add(assetType, asset)

        elif assetType == AssetManager.AssetType.Texture2DAsset:
            asset: Texture2D = Texture2D.Create(path)
            self.Add(assetType, asset)

        elif assetType == AssetManager.AssetType.MeshAsset:
            assets: List[Mesh] = Mesh.Load(path)
            asset = assets[0]

            for _asset in assets:
                self.Add(assetType, _asset)

        return asset

    def Get(self, name: str) -> Any:
        asset = self.__ShaderMap.get(name, None)
        if asset == None: asset = self.__Texture2DMap.get(name, None)
        if asset == None: asset = self.__MeshMap.get(name, None)
        return asset
