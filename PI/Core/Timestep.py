class Timestep:
    __Time: float

    def __init__(self, time: float=0.0) -> None:
        self.__Time = time

    @property
    def Seconds(self) -> float:
        return self.__Time

    @property
    def Milliseconds(self) -> float:
        return self.__Time * 1000.0
