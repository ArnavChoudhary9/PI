from typing import Any
from .Shader  import Shader
from .Texture import Texture2D

from ..logger import PI_CORE_ASSERT

class AssetManager:
    class AssetType:
        ShaderAsset, Texture2DAsset = range(0, 2)

    __slots__ = "__ShaderMap", "__TextureMap"

    def __init__(self) -> None:
        self.__ShaderMap  : dict = {}
        self.__TextureMap : dict = {}

    def Add(self, assetType: int, asset) -> None:
        if assetType == AssetManager.AssetType.ShaderAsset:
            PI_CORE_ASSERT(self.__ShaderMap.get(asset, True), "Asset already added. Asset: <Shader>: {}", asset)
            self.__ShaderMap[asset.Name] = asset

        if assetType == AssetManager.AssetType.Texture2DAsset:
            PI_CORE_ASSERT(self.__TextureMap.get(asset, True), "Asset already added. Asset: <Texture2D>: {}", asset)
            self.__TextureMap[asset.Name] = asset

    def Load(self, assetType: int, path: str) -> Any:
        asset = None

        if assetType == AssetManager.AssetType.ShaderAsset:
            asset: Shader = Shader.Create(path)
            self.Add(assetType, asset)

        if assetType == AssetManager.AssetType.Texture2DAsset:
            asset: Texture2D = Texture2D.Create(path)
            self.Add(assetType, asset)

        return asset

    def Get(self, name: str) -> Shader or Texture2D or None:
        asset = self.__ShaderMap.get(name, None)
        if asset == None: asset = self.__TextureMap.get(name, None)
        return asset
