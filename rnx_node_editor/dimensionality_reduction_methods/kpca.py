from .abstract_rd_method import RDMethod
from numpy import ndarray
from pandas import DataFrame
from sklearn.decomposition import KernelPCA


class KPCA(RDMethod):

    def __init__(self, n_components):
        super().__init__(n_components, "KPCA")

    def spectrum(self, X:ndarray) -> DataFrame:

        super().dimension_parameter_is_wrong(self.n_components, X.shape[1])

        transformer = KernelPCA(n_components=self.n_components, kernel='sigmoid')
        X_transformed = transformer.fit_transform(X)

        return super().data_frame(X_transformed)
