from .abstract_rd_method import RDMethod
from numpy import ndarray
from pandas import DataFrame
from sklearn.manifold import MDS as mds


class MDS(RDMethod):

    def __init__(self, n_components):
        super().__init__(n_components, "MDS")

    def spectrum(self, X: ndarray) -> DataFrame:
        super().dimension_parameter_is_wrong(self.n_components, X.shape[1])

        embedding = mds(n_components=self.n_components)
        X_transformed = embedding.fit_transform(X)

        return super().data_frame(X_transformed)