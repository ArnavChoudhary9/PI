from .Event import Event, EventType, EventCategory

class WindowResizeEvent(Event):
    __Width: int
    __Height: int

    def __init__(self, width: int, height: int) -> None:
        self.__Width = width
        self.__Height = height

    @property
    def Width(self) -> int:
        return self.__Width

    @property
    def Height(self) -> int:
        return self.__Height

    @property
    def EventType(self) -> int:
        return EventType.WindowResize

    @property
    def CategoryFlags(self) -> int:
        return EventCategory.Application

    def ToString(self) -> str:
        return "<WindowResizeEvent: {}, {}>".format(self.__Width, self.__Height)

class WindowCloseEvent(Event):
    def __init__(self) -> None:
        pass

    @property
    def EventType(self) -> int:
        return EventType.WindowClose

    @property
    def CategoryFlags(self) -> int:
        return EventCategory.Application

    def ToString(self) -> str:
        return "<WindowCloseEvent>"

class WindowFocusEvent(Event):
    def __init__(self) -> None:
        pass

    @property
    def EventType(self) -> int:
        return EventType.WindowFocus

    @property
    def CategoryFlags(self) -> int:
        return EventCategory.Application

    def ToString(self) -> str:
        return "<WindowFocusEvent>"  

class WindowMovedEvent(Event):
    __offsetX: int
    __offsetY: int

    def __init__(self, offsetX: int, offsetY: int) -> None:
        self.__offsetX = offsetX
        self.__offsetY = offsetY

    @property
    def offsetX(self) -> int:
        return self.__offsetX

    @property
    def offsetY(self) -> int:
        return self.__offsetY

    @property
    def EventType(self) -> int:
        return EventType.WindowMoved

    @property
    def CategoryFlags(self) -> int:
        return EventCategory.Application

    def ToString(self) -> str:
        return "<WindowMovedEvent: {}, {}>".format(self.__offsetX, self.__offsetY)

class AppTickEvent(Event):
    def __init__(self) -> None:
        pass

    @property
    def EventType(self) -> int:
        return EventType.AppTick

    @property
    def CategoryFlags(self) -> int:
        return EventCategory.Application

    def ToString(self) -> str:
        return "<AppTickEvent>"  

class AppUpdateEvent(Event):
    def __init__(self) -> None:
        pass

    @property
    def EventType(self) -> int:
        return EventType.AppUpdate

    @property
    def CategoryFlags(self) -> int:
        return EventCategory.Application

    def ToString(self) -> str:
        return "<AppUpdateEvent>"  

class AppRenderEvent(Event):
    def __init__(self) -> None:
        pass

    @property
    def EventType(self) -> int:
        return EventType.AppRender

    @property
    def CategoryFlags(self) -> int:
        return EventCategory.Application

    def ToString(self) -> str:
        return "<AppRenderEvent>"  
