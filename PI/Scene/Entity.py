from .Components import TransformComponent
from ..Logging import PI_CLIENT_ASSERT, PI_CLIENT_WARN

from typing import TypeVar as _TypeVar
from typing import Type    as _Type

_C = _TypeVar("_C")

class Entity():
    __EntityHandle : int   = None
    __Scene                = None

    def __init__(self, entityHandle: int, scene) -> None:
        self.__EntityHandle = entityHandle
        self.__Scene = scene

    def __int__  (self) -> int  : return self.__EntityHandle
    def __bool__ (self) -> bool : return self.__EntityHandle != None
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Entity): return False
        return ((self.__EntityHandle == other.__EntityHandle) and (self.__Scene == other.__Scene))
    def __ne__(self, other) -> bool: return not (self == other)

    def AddComponent(self, componentType: _Type[_C], *args, **kwargs) -> _C:
        PI_CLIENT_ASSERT(not self.HasComponent(componentType),
            "Enitiy: {} ({}), Already have component of type: {}", self, int(self), componentType
        )

        component = componentType(*args, **kwargs)
        self.__Scene._Registry.add_component(self.__EntityHandle, component)
        self.__Scene._OnComponentAdded(self, component)
        return component

    def GetComponent(self, componentType: _Type[_C]) -> _C:
        PI_CLIENT_ASSERT(self.HasComponent(componentType),
            "Enitiy: {} ({}), Does not have component of type: {}", self, int(self), componentType
        )

        entities = self.__Scene._Registry.get_component(componentType)
        for entity, componentType in entities:
            if self.__EntityHandle == entity:
                return componentType

    def HasComponent(self, componentType: _Type[_C]) -> bool:
        return self.__Scene._Registry.has_component(self.__EntityHandle, componentType)

    def RemoveComponent(self, componentType: _Type[_C]) -> None:
        PI_CLIENT_ASSERT(self.HasComponent(componentType),
            "Enitiy: {} ({}), Does not have component of type: {}", self, int(self), componentType
        )
        if componentType is TransformComponent:
            PI_CLIENT_WARN("Trying to remove Transform Component from an Entity.")
            return

        self.__Scene._Registry.remove_component(self.__EntityHandle, componentType)
