from rnx_node_editor.dimensionality_reduction_methods.pca import PCA
from rnx_node_editor.dimensionality_reduction_methods.le import LE
from rnx_node_editor.dimensionality_reduction_methods.lle import LLE
from rnx_node_editor.dimensionality_reduction_methods.kpca import KPCA
from rnx_node_editor.dimensionality_reduction_methods.mds import MDS
from rnx_node_editor.dimensionality_reduction_methods.isomap import ISOMAP
from rnx_node_editor.examples.example_calculator.data_class.FileSystemDataRepository import FileSystemRepository
from rnx_node_editor.examples.example_calculator.views import scatter_plot, line_plot
import  numpy as np
from rnx_node_editor.rnx.score_rnx import ScoreRnx
repo = FileSystemRepository()
from pandas import  DataFrame

# bases de datos
#mnist = repo.load("C:\\Users\\Diego\\Desktop\\datos de prueba\\mnist_train_1.mat")
#ataque = repo.load("C:\\Users\\Diego\\Desktop\\datos de prueba\\ataque_corazon.mat")
#faces = repo.load("C:\\Users\\Diego\\Desktop\\datos de prueba\\faces.mat")
#swis = repo.load("D:\\rnx_tool\\rnx_tool\\rnx_node_editor\\examples\\example_calculator\\data\\data_swissroll.mat")
iris = repo.load("C:\\Users\\Diego\\Desktop\\rnx_tool\\data\\iris.csv", ",")
#esfera = repo.load("C:\\Users\\Diego\\Desktop\\rnx_tool\\test\\esfera.mat")
#toroide = repo.load("C:\\Users\\Diego\\Desktop\\rnx_tool\\test\\toroide.mat")
#print(DataFrame(toroide))

#MNIST = repo.load("C:\\Users\\Diego\Desktop\\datos de prueba\\mnist_1000_ok")

# metodos
#LE = repo.load("C:\\Users\\Diego\\Desktop\\datos de prueba\\METODOS\\LE_MNIST_1000.mat")
#LLE = repo.load("C:\\Users\\Diego\\Desktop\\datos de prueba\\METODOS\\LLE_MNIST_1000.mat")
#PCA = repo.load("C:\\Users\\Diego\\Desktop\\datos de prueba\\METODOS\\PCA_MNIST_1000.mat")
print(iris)
iris.pop('virginica')
print(iris)

kpca = KPCA(2)
response_kpca = kpca.spectrum(iris)

le = LE(2,10)
response_le = le.spectrum(iris)

lle = LLE(2,10)
response_lle = lle.spectrum(iris)

isomap = ISOMAP(2,10)
response_iso = isomap.spectrum(iris)


rnx_le = ScoreRnx(iris, response_le)
rnx_le.run()

rnx_lle = ScoreRnx(iris, response_lle)
rnx_lle.run()

rnx_isomap = ScoreRnx(iris, response_iso)
rnx_isomap.run()

rnx_kpca = ScoreRnx(iris, response_kpca)
rnx_kpca.run()

list = [
    {
    'title': 'KPCA',
    'rnx': rnx_kpca.get_rnx()[1],
    'score': rnx_kpca.get_rnx()[0]
    },
    {
        'title': 'LE',
        'rnx': rnx_le.get_rnx()[1],
        'score': rnx_le.get_rnx()[0]
    },
    {
        'title': 'LLE',
        'rnx': rnx_lle.get_rnx()[1],
        'score': rnx_lle.get_rnx()[0]
    },
    {
        'title': 'ISOMAP',
        'rnx': rnx_isomap.get_rnx()[1],
        'score': rnx_isomap.get_rnx()[0]
    }
]


line_plot.line_chart(list)
scatter_plot.view(2,response_lle)
scatter_plot.view(2,response_le)
scatter_plot.view(2, response_iso)
scatter_plot.view(2,response_kpca)





