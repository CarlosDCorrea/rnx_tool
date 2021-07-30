from .abstract_rd_method import RDMethod
from pandas import DataFrame
from numpy import ndarray
from sklearn.decomposition import PCA as pca_sk


class PCA(RDMethod):

    def __init__(self, n_components):
        super().__init__(n_components, "PCA")

    def spectrum(self, X: ndarray) -> DataFrame:
        super().dimension_parameter_is_wrong(self.n_components, X.shape[1])
        pca = pca_sk(n_components=self.n_components)
        pca = pca.fit(X)
        X_transformed = pca.transform(X)
        self.components = super().data_frame(X_transformed)
        return super().data_frame(X_transformed)