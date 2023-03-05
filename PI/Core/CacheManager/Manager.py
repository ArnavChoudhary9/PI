from ..Base import PI_VERSION

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

class CacheLoadingError(Exception): pass

class LocalCache:
    __Fields: Dict[str, Any]

    @staticmethod
    def Init():
        LocalCache.__Fields = {}
        Cache.InitLocalTempDirectory()
        return LocalCache
    
    @staticmethod
    def GetData() -> Dict[str, Any]: return LocalCache.__Fields

    @staticmethod
    def SetProperty(name: str, value: Any):
        LocalCache.__Fields[name] = value
        return LocalCache

    @staticmethod
    def SetProperties(**NameValuePaires: Dict[str, Any]):
        for name, value in NameValuePaires.items(): LocalCache.__Fields[name] = value
        return LocalCache

    @staticmethod
    def SetPropertiesFromDict(nameValuePaires: Dict[str, Any]):
        for name, value in nameValuePaires.items(): LocalCache.__Fields[name] = value
        return LocalCache

    @staticmethod
    def GetProperty(name: str, default=None) -> Any: return LocalCache.__Fields.get(name, default)

    @staticmethod
    def GetProperties(*Names: List[str]) -> Dict[str, Any]:
        fields = {}
        for name in Names: fields[name] = LocalCache.__Fields.get(name, None)
        return fields

    @staticmethod
    def DeleteProperty(*properties: Tuple[str]):
        for property in properties:
            if property in LocalCache.__Fields.keys():
                del LocalCache.__Fields[property]
        return LocalCache

    @staticmethod
    def DumpFields():
        LocalCache.SetProperty("Version", PI_VERSION)
        with open(f"{Cache.GetLocalSaveDirectory()}\\LocalCache.json", 'w') as f: json.dump(LocalCache.__Fields, f)
        return LocalCache

    @staticmethod
    def __LoadFields(_depth: int=10):
        if _depth == 0: raise CacheLoadingError("Error loading cache. Max depth reached.")

        LocalCache.__Fields = {}
        try:
            with open(f"{Cache.GetLocalSaveDirectory()}\\LocalCache.json", 'r') as f:
                LocalCache.__Fields = json.load(f)
        except Exception as _:
            LocalCache.DumpFields()
            return LocalCache.__LoadFields(_depth-1)

        # Cache invalidation
        finally:
            version = LocalCache.GetProperty("Version", None)

            if not version: LocalCache.SetProperty("Version", PI_VERSION)
            elif version != PI_VERSION:
                # LocalCache.__Fields.clear()
                try: del LocalCache.__Fields["ProjectSettings"]
                except KeyError as _: pass

                LocalCache.DumpFields()
                return LocalCache.__LoadFields(_depth-1)

        return LocalCache

    @staticmethod
    def LoadFields(): return LocalCache.__LoadFields()

    @staticmethod
    def Shutdown():
        LocalCache.DumpFields()
        LocalCache.__Fields = {}
        return None
