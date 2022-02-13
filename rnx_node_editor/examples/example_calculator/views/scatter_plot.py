import matplotlib.pyplot as plt
from pandas import DataFrame
from numpy import ndarray


def view_3d(node, data):
    title = node.title
    x, y, z = data['component1'], data['component2'], data['component3']

    plt.figure(figsize=(6, 6))
    ax = plt.axes(projection="3d")
    plt.title(title)
    ax.scatter3D(x, y, z, c=z, cmap="plasma")
    plt.show()


def view(dimension, data):
    #title = node.title
    plt.figure(figsize=(5, 4))
    ax = plt.axes()
   # plt.title(title)

    if dimension == 2:
        """
        Algunas validaciones que se deben tener en cuenta:
        - se debe preguntar si los datos son reales o artificiales
            - Si los datos son artificiales se puede usar "component1..."
            - Si no, se debe traer los labels del data set real
        - Si los datos son reales se usará rgb para representar dichos puntos, esto aplica
        para tres dimensiones también
        """
        x, y = data['component1'], data['component2']
        ax.scatter(x, y, c=y, cmap='plasma')
        plt.xlabel(data.columns[0])
        plt.ylabel(data.columns[1])

    elif dimension == 1:
        pass

    plt.show()
