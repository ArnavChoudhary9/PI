from watchdog.events    import FileSystemEventHandler as _FSEventHandler
from watchdog.events    import FileCreatedEvent, FileModifiedEvent, FileDeletedEvent, FileSystemMovedEvent
from watchdog.observers import Observer as _Observer

import pathlib

from typing import Type

class FileSystemEventHandler:
    @staticmethod
    def OnCreated  ( event: FileCreatedEvent     ) -> None: ...
    @staticmethod
    def OnModified ( event: FileModifiedEvent    ) -> None: ...
    @staticmethod
    def OnDeleted  ( event: FileDeletedEvent     ) -> None: ...
    @staticmethod
    def OnMoved    ( event: FileSystemMovedEvent ) -> None: ...

class DirectoryWatcher:
    __EventHandler : _FSEventHandler
    __Observer     : Type[_Observer]
    __Directory    : pathlib.Path

    def __init__(self, directory: pathlib.Path, eventHandler: FileSystemEventHandler) -> None:
        self.__Directory = directory

        self.__EventHandler = _FSEventHandler()
        self.__EventHandler.on_created  = eventHandler.OnCreated
        self.__EventHandler.on_modified = eventHandler.OnModified
        self.__EventHandler.on_deleted  = eventHandler.OnDeleted
        self.__EventHandler.on_moved    = eventHandler.OnMoved

        self.__Observer = _Observer()

    @property
    def Directory(self) -> pathlib.Path: self.__Directory

    def Start(self) -> None:
        self.__Observer.schedule(self.__EventHandler, str(self.__Directory), True)
        self.__Observer.start()

    def Stop(self) -> None:
        self.__Observer.stop()
        self.__Observer.join()
