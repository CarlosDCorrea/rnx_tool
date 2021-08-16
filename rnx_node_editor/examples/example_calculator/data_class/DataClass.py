from numpy import ndarray

class Data:

    def __init__(self, components: ndarray, path: str) -> None:
        self.__components = components
        self.__path = path
        self.headers = None

    def getPath(self) -> str:
        return self.__path
    
    def getComponents(self) -> ndarray :
        return self.__components

    
    def __len__(self):
        return len(self.__components)

    def __shape__(self):
        return self.__components.shape
