from .Event import Event, EventType, EventCategory

class MouseEvent(Event):
    def __init__(self) -> None:
        pass

    @property
    def CategoryFlags(self) -> int:
        return EventCategory.Mouse | EventCategory.Input

class MouseButtonPressedEvent(MouseEvent):
    __slots__ = "__ButtonCode"

    def __init__(self, buttonCode: int) -> None:
        self.__ButtonCode = buttonCode

    @property
    def ButtonCode(self) -> int:
        return self.__ButtonCode

    @property
    def EventType(self) -> int:
        return EventType.MouseButtonPressed

    @property
    def CategoryFlags(self) -> int:
        return super().CategoryFlags | EventCategory.MouseButton

    def ToString(self) -> str:
        return "<MouseButtonPressedEvent: {}>".format(self.__ButtonCode)
        
class MouseButtonReleasedEvent(MouseEvent):
    __slots__ = "__ButtonCode"

    def __init__(self, buttonCode: int) -> None:
        self.__ButtonCode = buttonCode

    @property
    def ButtonCode(self) -> int:
        return self.__ButtonCode

    @property
    def EventType(self) -> int:
        return EventType.MouseButtonReleased

    @property
    def CategoryFlags(self) -> int:
        return super().CategoryFlags | EventCategory.MouseButton

    def ToString(self) -> str:
        return "<MouseButtonReleasedEvent: {}>".format(self.__ButtonCode)

class MouseMovedEvent(MouseEvent):
    __slots__ = "__OffsetX", "__OffsetY"

    def __init__(self, offsetX: int, offsetY: int) -> None:
        self.__OffsetX = offsetX
        self.__OffsetY = offsetY

    @property
    def OffsetX(self) -> int:
        return self.__OffsetX

    @property
    def OffsetY(self) -> int:
        return self.__OffsetY

    @property
    def EventType(self) -> int:
        return EventType.MouseMoved

    def ToString(self) -> str:
        return "<MouseMovedEvent: {}, {}>".format(self.__OffsetX, self.__OffsetY)

class MouseScrolledEvent(MouseEvent):
    __slots__ = "__OffsetX", "__OffsetY"

    def __init__(self, offsetY: int, offsetX: int=0) -> None:
        self.__OffsetX = offsetX
        self.__OffsetY = offsetY

    @property
    def OffsetX(self) -> int:
        return self.__OffsetX

    @property
    def OffsetY(self) -> int:
        return self.__OffsetY

    @property
    def EventType(self) -> int:
        return EventType.MouseScrolled

    def ToString(self) -> str:
        return "<MouseScrolledEvent: {}, {}>".format(self.__OffsetX, self.__OffsetY)
