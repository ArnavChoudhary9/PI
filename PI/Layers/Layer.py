from ..Events import Event

class Layer:
    __slots__ = "_DebugName", "_IsEnable"

    def __init__(self, name: str="Layer") -> None:
        self._DebugName = name
        self._IsEnable  = True

    def OnAttach(self) -> None:
        pass

    def OnDetach(self) -> None:
        pass

    def OnUpdate(self, timestep=0.0) -> None:
        pass

    def OnEvent(self, event: Event) -> None:
        pass

    def OnImGuiRender(self) -> None:
        pass

    def ToggleEnable(self) -> None:
        self._IsEnable = not self._IsEnable

    def SetEnable(self, enable: bool) -> None:
        self._IsEnable = enable

    @property
    def IsEnable(self) -> bool:
        return self._IsEnable

    @property
    def Name(self) -> str:
        return self._DebugName
