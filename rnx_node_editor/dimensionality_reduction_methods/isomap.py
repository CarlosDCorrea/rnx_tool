from .abstract_rd_method import RDMethod
from numpy import ndarray
from pandas import DataFrame
from sklearn.manifold import Isomap


class ISOMAP(RDMethod):
    def __init__(self, n_components, n_neighbours):
        super().__init__(n_components, "ISOMAP", n_neighbours)

    def spectrum(self, X:ndarray) -> DataFrame:
        super().dimension_parameter_is_wrong(self.n_components, X.shape[1])

        embedding = Isomap(n_components=self.n_components, n_neighbors=self.n_neighbours)
        X_transformed = embedding.fit_transform(X)

        return super().data_frame(X_transformed)