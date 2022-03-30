from .Layer import Event, Layer

class LayerStack:
    __slots__ = "__Layers", "__LayerInsertPos"
    
    def __init__(self) -> None:
        self.__Layers: list = []
        self.__LayerInsertPos = 0

    def __del__(self) -> None:
        for i in range(0, self.length-1):
            del self.__Layers[i]

    def PushLayer(self, layer: Layer) -> None:
        self.__Layers.insert(self.__LayerInsertPos, layer)
        self.__LayerInsertPos += 1

        layer.OnAttach()

    def PushOverlay(self, overlay: Layer) -> None:
        self.__Layers.append(overlay)
        overlay.OnAttach()

    def PopLayer(self, layer: Layer) -> None:
        if self.length > 0:
            self.__Layers.remove(layer)
            self.__LayerInsertPos -= 1

            layer.OnDetach()

        else:
            pass

    def PopOverlay(self, overlay: Layer) -> None:
        if self.length > 0:
            self.__Layers.remove(overlay)
            overlay.OnDetach()

        else:
            pass

    def OnUpdate(self, timestep=0.0) -> None:
        for layer in self.__Layers:
            layer.OnUpdate(timestep)

    def OnImGuiRender(self) -> None:
        for layer in self.__Layers:
            layer.OnImGuiRender()

    def OnEvent(self, event: Event) -> bool:
        layers = self.__Layers.copy()
        layers.reverse()

        for layer in layers:
            layer.OnEvent(event)
            
            if (event.Handled):
                return True

        return False

    @property
    def length(self) -> int:
        return len(self.__Layers)

    @property
    def begin(self) -> Layer:
        if self.__LayerInsertPos > 0:
            return self.__Layers[0]
        else:
            return None

    @property
    def end(self) -> Layer:
        if self.__LayerInsertPos > 0:
            return self.__Layers[len(self.__Layers)-1]
        else:
            return None

    @property
    def GetLastLayer(self) -> Layer:
        if self.__LayerInsertPos > 0:
            return self.__Layers[self.__LayerInsertPos-1]
        else:
            return None
