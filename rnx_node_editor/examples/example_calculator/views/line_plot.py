import matplotlib.pyplot as plt
import matplotlib.cm as cm
from pandas import DataFrame
import numpy as np
from numpy import ndarray


def line_chat(node):
    bottom, top = 0, 100
    plt.plot(np.arange(len(node.y)), 100 * node.y, label=f"{node.previous_method_name}:{round(node.score * 100, 3)}%")
    plt.xscale('log')
    plt.ylim(bottom, top)
    plt.legend()
    plt.show()
