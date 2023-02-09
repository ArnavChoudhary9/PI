import os
import json
from tempfile import gettempdir

from typing import Dict, Any, List

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

class Settings:
    __Data: Dict[str, Any]

    @staticmethod
    def Init():
        Settings.__Data = {}
        Cache.InitLocalTempDirectory()
        return Settings
    
    @staticmethod
    def GetData() -> Dict[str, Any]: return Settings.__Data

    @staticmethod
    def SetProperty(name: str, value: Any):
        Settings.__Data[name] = value
        return Settings

    @staticmethod
    def SetProperties(**NameValuePaires: Dict[str, Any]):
        for name, value in NameValuePaires.items(): Settings.__Data[name] = value
        return Settings

    @staticmethod
    def SetPropertiesFromDict(nameValuePaires: Dict[str, Any]):
        for name, value in nameValuePaires.items(): Settings.__Data[name] = value
        return Settings

    @staticmethod
    def GetProperty(name: str) -> Any: return Settings.__Data.get(name, None)

    @staticmethod
    def GetProperties(*Names: List[str]) -> Dict[str, Any]:
        fields = {}
        for name in Names: fields[name] = Settings.__Data.get(name, None)
        return fields

    @staticmethod
    def DumpFields():
        with open(f"{Cache.GetLocalSaveDirectory()}\\Settings.json", 'w') as f: json.dump(Settings.__Data, f)
        return Settings

    @staticmethod
    def LoadFields():
        Settings.__Data = {}
        with open(f"{Cache.GetLocalSaveDirectory()}\\Settings.json", 'r') as f: Settings.__Data = json.load(f)
        return Settings

    @staticmethod
    def Shutdown():
        Settings.DumpFields()
        Settings.__Data = {}
        return None
