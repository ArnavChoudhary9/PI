from .Event import Event, EventCategory, EventType

class KeyEvent(Event):
    _KeyCode: int

    def __init__(self, keyCode: int) -> None:
        self._KeyCode = keyCode

    @property
    def KeyCode(self) -> int:
        return self._KeyCode

    @property
    def CategoryFlags(self) -> int:
        return EventCategory.Keyboard | EventCategory.Input

class KeyPressedEvent(KeyEvent):
    _RepeatCount: int

    def __init__(self, keyCode: int, repeatCount: int) -> None:
        super().__init__(keyCode)
        self._RepeatCount = repeatCount

    @property
    def EventType(self) -> int:
        return EventType.KeyPressed

    def ToString(self) -> str:
        return "<KeyPressedEvent: {} ({} repeats)>".format(self._KeyCode, self._RepeatCount)

class KeyReleasedEvent(KeyEvent):
    def __init__(self, keyCode: int) -> None:
        super().__init__(keyCode)

    @property
    def EventType(self) -> int:
        return EventType.KeyReleased

    def ToString(self) -> str:
        return "<KeyReleasedEvent: {}>".format(self._KeyCode)
