from rnx_node_editor.examples.example_calculator.data_class.FileSystemDataRepository import FileSystemRepository
from rnx_node_editor.rnx.score_rnx import ScoreRnx
from pandas import  DataFrame
import numpy as np
repo = FileSystemRepository()

# Datos en alta dimension
#swissroll = repo.load("D:\\rnx_tool\\rnx_tool\\rnx_node_editor\\examples\\example_calculator\\data\\data_swissroll.mat")
#mnist = repo.load("C:\\Users\\Diego\\Desktop\\datos de prueba\\mnist_train_1.mat")
coil = repo.load("C:\\Users\\Diego\\Desktop\\datos de prueba\\coil_1440.mat")

#swissroll_matlab_mds = repo.load("C:\\Users\\Diego\\Desktop\\rnx_tool\\test\\rollo suizo\\mds.mat")
#swissroll_matlab_pca = repo.load("C:\\Users\\Diego\\Desktop\\rnx_tool\\test\\rollo suizo\\pca.mat")
#swissroll_matlab_le = repo.load("C:\\Users\\Diego\\Desktop\\rnx_tool\\test\\rollo suizo\\le_k_10.mat")

#mnist_matlab_pca = repo.load("C:\\Users\\Diego\\Desktop\\datos de prueba\\METODOS\\PCA_MNIST.mat")
coil_matlab_pca = repo.load()
# TEST WITH SWISROLL DATA
test_1 = ScoreRnx(coil, swissroll_matlab_pca)
test_1.run()

#test_2 = ScoreRnx(swissroll, swissroll_matlab_le)
#test_2.run()

#est_3 = ScoreRnx(swissroll, swissroll_matlab_mds)
#test_3.run()

print("=============TEST===============")

print("Test 1 swisrool with pca =>", test_1.get_rnx()[0])
#print("Test 2 swisrool with le =>", test_2.get_rnx()[0])
#print("Test 3 swisrool with mds =>", test_3.get_rnx()[0])

