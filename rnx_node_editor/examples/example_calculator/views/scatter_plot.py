import matplotlib.pyplot as plt
from pandas import DataFrame
from numpy import ndarray


def view_3d(X:ndarray):
    x, y, z = X[:, 0], X[:, 1], X[:, 2]

    fig = plt.figure(figsize=(5, 4))

    ax = plt.axes(projection="3d")

    ax.scatter3D(x, y, z, c=z, cmap="plasma")

    plt.show()

def view(X_transformed:DataFrame):

    x, y = X_transformed['component1'], X_transformed['component2']

    fig = plt.figure(figsize=(5, 4))
    ax = plt.axes()

    ax.scatter(x, y, c=y, cmap='plasma')

    plt.xlabel(X_transformed.columns[0])
    plt.ylabel(X_transformed.columns[1])

    plt.show()
