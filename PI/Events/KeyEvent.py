from .Event import Event, EventCategory, EventType

class KeyEvent(Event):
    __slots__ = "_KeyCode"

    def __init__(self, keyCode: int) -> None:
        self._KeyCode = keyCode

    @property
    def KeyCode(self) -> int:
        return self._KeyCode

    @property
    def CategoryFlags(self) -> int:
        return EventCategory.Keyboard | EventCategory.Input

class KeyPressedEvent(KeyEvent):
    __slots__ = "_RepeatCount"

    def __init__(self, keyCode: int, repeatCount: int) -> None:
        super().__init__(keyCode)
        self._RepeatCount = repeatCount

    @property
    def EventType(self) -> int:
        return EventType.KeyPressed

    def ToString(self) -> str:
        return "<KeyPressedEvent: {} ({} repeats)>".format(self._KeyCode, self._RepeatCount)

class CharInputEvent(KeyEvent):
    __slots__ = "__Char"

    def __init__(self, char: int) -> None:
        # super().__init__(char)
        self.__Char = char

    @property
    def Char(self):
        return self.__Char

    @property
    def EventType(self) -> int:
        return EventType.CharInput

    @property
    def CategoryFlags(self) -> int:
        return EventCategory.Keyboard | EventCategory.Input

    def ToString(self) -> str:
        return "<CharInputEvent: {}>".format(self._KeyCode)

class KeyReleasedEvent(KeyEvent):
    def __init__(self, keyCode: int) -> None:
        super().__init__(keyCode)

    @property
    def EventType(self) -> int:
        return EventType.KeyReleased

    def ToString(self) -> str:
        return "<KeyReleasedEvent: {}>".format(self._KeyCode)
