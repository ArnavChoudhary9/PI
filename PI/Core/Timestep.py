class Timestep:
    '''Basic helper class for managing the the deltas throughout the Application'''
    Scale: float = 1.0          # Universal scale
    GameScale: float = 1.0      # This Scale is only applied if asked

    __Time: float

    def __init__(self, time: float=0.0) -> None:
        self.__Time = time

    def __call__(self) -> float:
        '''Returns time in seconds'''
        return self.__Time * Timestep.Scale

    def __float__(self) -> float:
        '''Returns time in seconds'''
        return self.__Time * Timestep.Scale

    @property
    def Seconds(self) -> float:
        '''Returns time in seconds'''
        return self.__Time * Timestep.Scale

    @property
    def Milliseconds(self) -> float:
        '''Returns time in Milliseconds'''
        return self.__Time * Timestep.Scale * 1000.0
    
    @property
    def GameDelta(self) -> float:
        '''Returns time in seconds (Game Scale is also applied)'''
        return self.__Time * Timestep.Scale * Timestep.GameScale

    @property
    def FixedTime(self) -> float:
        '''Returns time in seconds (Scale is not applied)'''
        return self.__Time
