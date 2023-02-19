import os
import json
from tempfile import gettempdir

from typing import Dict, Any, List, Tuple

class Cache:
    __TempDirGenerated = False

    @staticmethod
    def InitLocalTempDirectory():
        if not Cache.__TempDirGenerated:
            os.makedirs(f"{gettempdir()}\\PI", exist_ok=True)
            os.makedirs("C:\\ProgramData\\PI", exist_ok=True)
            Cache.__TempDirGenerated = True

        return Cache

    @staticmethod
    def GetLocalTempDirectory():
        Cache.InitLocalTempDirectory()
        return f"{gettempdir()}\\PI"

    @staticmethod
    def GetLocalSaveDirectory():
        Cache.InitLocalTempDirectory()
        return "C:\\ProgramData\\PI"

class LocalCache:
    __Data: Dict[str, Any]

    @staticmethod
    def Init():
        LocalCache.__Data = {}
        Cache.InitLocalTempDirectory()
        return LocalCache
    
    @staticmethod
    def GetData() -> Dict[str, Any]: return LocalCache.__Data

    @staticmethod
    def SetProperty(name: str, value: Any):
        LocalCache.__Data[name] = value
        return LocalCache

    @staticmethod
    def SetProperties(**NameValuePaires: Dict[str, Any]):
        for name, value in NameValuePaires.items(): LocalCache.__Data[name] = value
        return LocalCache

    @staticmethod
    def SetPropertiesFromDict(nameValuePaires: Dict[str, Any]):
        for name, value in nameValuePaires.items(): LocalCache.__Data[name] = value
        return LocalCache

    @staticmethod
    def GetProperty(name: str, default=None) -> Any: return LocalCache.__Data.get(name, default)

    @staticmethod
    def GetProperties(*Names: List[str]) -> Dict[str, Any]:
        fields = {}
        for name in Names: fields[name] = LocalCache.__Data.get(name, None)
        return fields

    @staticmethod
    def DeleteProperty(*properties: Tuple[str]):
        for property in properties:
            if property in LocalCache.__Data.keys():
                del LocalCache.__Data[property]
        return LocalCache

    @staticmethod
    def DumpFields():
        with open(f"{Cache.GetLocalSaveDirectory()}\\LocalCache.json", 'w') as f: json.dump(LocalCache.__Data, f)
        return LocalCache

    @staticmethod
    def LoadFields():
        LocalCache.__Data = {}
        try:
            with open(f"{Cache.GetLocalSaveDirectory()}\\LocalCache.json", 'r') as f: LocalCache.__Data = json.load(f)
        except Exception as _:
            LocalCache.DumpFields()
            return LocalCache.LoadFields()
        return LocalCache

    @staticmethod
    def Shutdown():
        LocalCache.DumpFields()
        LocalCache.__Data = {}
        return None
