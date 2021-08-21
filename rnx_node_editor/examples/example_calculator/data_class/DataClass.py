from numpy import ndarray
from pandas import DataFrame

class Data:

    def __init__(self, components: DataFrame) -> None:
        self.__components = components


    def getComponents(self) -> DataFrame :
        return self.__components

    def getHeader(self):
        return list(self.__components.columns.values)
    
    def __len__(self):
        return len(self.__components)

    def __shape__(self):
        return self.__components.shape
