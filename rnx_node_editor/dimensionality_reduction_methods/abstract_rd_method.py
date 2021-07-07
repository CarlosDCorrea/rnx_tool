from abc import ABC, abstractmethod
from numpy import ndarray
from pandas import DataFrame


class RDMethod(ABC):

    def __init__(self, n_components, name, n_neighbours=None):
        self.n_components = n_components
        self.n_neighbours = n_neighbours
        self.name = name
        self.components = []

    def get_name(self):
        return self.name

    def setComponents(self, data):
        self.components = data

    def dimension_parameter_is_wrong(self, n_components, X_dimension):
        print(X_dimension)
        if n_components > X_dimension:
            raise Exception("La dimensión debe ser menor o igual a la dimensión del data set")

    def data_frame(self, X_transformed: ndarray) -> DataFrame:

        data = {}

        cols = ['component' + str(i) for i in range(1, self.n_components + 1)]

        for i in range(len(cols)):
            data[cols[i]] = X_transformed[:, i]

        return DataFrame(data)

    @abstractmethod
    def spectrum(self, X:ndarray) -> DataFrame:
        pass