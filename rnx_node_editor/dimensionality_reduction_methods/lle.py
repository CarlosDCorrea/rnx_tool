from pandas import DataFrame
from .abstract_rd_method import RDMethod
from numpy import ndarray
from sklearn.manifold import LocallyLinearEmbedding

class LLE(RDMethod):

    def __init__(self, n_components, n_neighbours):
        super().__init__(n_components, "LLE", n_neighbours)

    def spectrum(self, X: ndarray) -> DataFrame:

        super().dimension_parameter_is_wrong(self.n_components, X.shape[1])

        lle = LocallyLinearEmbedding(n_components = self.n_components, n_neighbors=self.n_neighbours)
        X_trasnformed = lle.fit_transform(X)

        return super().data_frame(X_trasnformed)