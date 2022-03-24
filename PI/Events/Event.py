# This just shifts 1 to i th BIT
def BIT(i: int) -> int:
    return int(1 << i)

# This class is equvalent to a C++ enum
class EventType:
    Null,                                                                   \
    WindowClose, WindowResize, WindowFocus, WindowMoved,                    \
    AppTick, AppUpdate, AppRender,                                          \
    KeyPressed, KeyReleased,                                                \
    MouseButtonPressed, MouseButtonReleased, MouseMoved, MouseScrolled      \
        = range(0, 14)

# This class is equvalent to a C++ enum

# It uses bitstream to represent flags, so
# a single Event can have multiple flags
class EventCategory:
    Null = 0
    Application    = BIT(0)
    Input          = BIT(1)
    Keyboard       = BIT(2)
    Mouse          = BIT(3)
    MouseButton    = BIT(4)

class Event:
    Handled = False

    @property
    def EventType(self) -> int:
        pass

    @property    
    def Name(self) -> str:
        return type(self)

    @property    
    def CategoryFlags(self) -> int:
        pass

    def ToString(self) -> str:
        return self.GetName()

    def IsInCategory(self, category: int) -> bool:
        return bool(self.CategoryFlags & category)

    def __repr__(self) -> str:
        return self.ToString()

class EventDispatcher:
    _Event: Event

    def __init__(self, event: Event=Event()) -> None:
        self._Event = event

    def ChangeEvent(self, event: Event):
        self._Event = event

    def Dispach(self, func, eventType: int) -> bool:
        if (self._Event.EventType == eventType):
            self._Event.Handled = func(self._Event)
            return True

        return False
