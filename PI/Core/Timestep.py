class Timestep:
    '''Basic helper class for managing the the deltas throughout the Application'''
    __Time: float

    def __init__(self, time: float=0.0) -> None:
        self.__Time = time

    def __call__(self) -> float:
        '''Returns time in seconds'''
        return self.__Time

    def __float__(self) -> float:
        '''Returns time in seconds'''
        return self.__Time

    @property
    def Seconds(self) -> float:
        '''Returns time in seconds'''
        return self.__Time

    @property
    def Milliseconds(self) -> float:
        '''Returns time in Milliseconds'''
        return self.__Time * 1000.0
