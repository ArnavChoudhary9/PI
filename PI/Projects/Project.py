from ..Core.Base   import PI_VERSION
from ..Logging     import PI_CLIENT_WARN, PI_CLIENT_TRACE
from ..Scene.Scene import Scene
from ..Utility.CacheManager.Manager import ProjectCache
from ..AssetManager.AssetManager import AssetManager
from ..Scripting.ScriptingEngine import ScriptingEngine

import os
import yaml
import pathlib

class Project:
    __Name    : str
    __ProjLoc : str

    __AssetsLoc  : str
    __ScriptLoc  : str
    __ScenesLoc  : str
    __StartScene : str

    def __init__(self, name: str="", projFileLoc: str=None, newLoc: str=None) -> None:
        self.__Name = name
        PI_CLIENT_TRACE(
            "New Project Initialized {} ({})", name,
            projFileLoc if projFileLoc is not None else newLoc
        )

        if projFileLoc is None:
            self.__ProjLoc    = "DefaultProject" if newLoc is None else newLoc
            self.__AssetsLoc  = "Assets"
            self.__ScriptLoc  = f"{self.__AssetsLoc}\\Scripts"
            self.__ScenesLoc  = f"{self.__AssetsLoc}\\Scenes"
            self.__StartScene = "DefaultScene.PI"

            self._InitDirs()

        else: self.Load(projFileLoc)

    @staticmethod
    def GetProjLocFromFileLoc(projFileLoc: str) -> str:
        if    projFileLoc.count("/") != 0: loc = "\\".join(projFileLoc.split("/")[:-1])
        else: loc = "\\".join(projFileLoc.split("\\")[:-1])
        return loc

    def _InitDirs(self) -> None:
        if not self.ProjectLocation.exists():
            os.mkdir(str( self.ProjectLocation .absolute() ))
            self.Save()

        if not self.AssetsLocation  .exists () : os.mkdir(str( self.AssetsLocation  .absolute() ))
        if not self.ScriptsLocation .exists () : os.mkdir(str( self.ScriptsLocation .absolute() ))
        if not self.ScenesLocation  .exists () : os.mkdir(str( self.ScenesLocation  .absolute() ))

        if not self.StartSceneLocation.exists():
            Scene.Serialize(Scene(), str(self.StartSceneLocation.absolute()))

        AssetManager()
        AssetManager().GetInstance().SetCurrentProjectLocation(str(self.AssetsLocation))

        ScriptingEngine .Init(str(self.ScriptsLocation))

        ProjectCache.DumpFields()
        ProjectCache.Init(str(self.ProjectLocation))
        ProjectCache.LoadFields()

    @property
    def ProjectLocation(self) -> pathlib.Path: return pathlib.Path(self.__ProjLoc)
    @property
    def AssetsLocation(self)  -> pathlib.Path: return pathlib.Path(f"{self.__ProjLoc}\\{self.__AssetsLoc}")
    @property
    def ScriptsLocation(self) -> pathlib.Path: return pathlib.Path(f"{self.__ProjLoc}\\{self.__ScriptLoc}")
    @property
    def ScenesLocation(self)  -> pathlib.Path: return pathlib.Path(f"{self.__ProjLoc}\\{self.__ScenesLoc}")
    @property
    def StartSceneLocation(self) -> pathlib.Path:
        return pathlib.Path(f"{self.__ProjLoc}\\{self.__ScenesLoc}\\{self.__StartScene}")
    
    @property
    def StartScene(self) -> Scene: return Scene.Deserialize(Scene(), str(self.StartSceneLocation))

    def Save(self):
        data = {}
        data["VERSION"] = PI_VERSION
        data["Project"] = {
            "Name": self.__Name,

            "ScriptLocation" : self.__ScriptLoc,
            "AssetsLocation" : self.__AssetsLoc,
            "ScenesLocation" : self.__ScenesLoc,
            "StartScene"     : self.__StartScene
        }

        path = f"{self.__ProjLoc}\\{self.__Name}.PIProj"
        with open(path, 'w') as f: yaml.dump(data, f)
        PI_CLIENT_TRACE("Current Project Saved!!")

    def Load(self, filename: str):
        data = {}
        with open(filename, 'r') as f: data = yaml.load(f, yaml.Loader)

        self.__ProjLoc = Project.GetProjLocFromFileLoc(filename)

        if data["VERSION"] != PI_VERSION: PI_CLIENT_WARN("Project version is old.")
        project = data["Project"]

        self.__Name = project["Name"]

        self.__ScriptLoc  = project["ScriptLocation"]
        self.__AssetsLoc  = project["AssetsLocation"]
        self.__ScenesLoc  = project["ScenesLocation"]
        self.__StartScene = project["StartScene"]

        self._InitDirs()
