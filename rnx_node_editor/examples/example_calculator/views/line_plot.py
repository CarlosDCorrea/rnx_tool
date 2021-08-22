import matplotlib.pyplot as plt
import matplotlib.cm as cm
from pandas import DataFrame
import numpy as np
from numpy import ndarray


def line_chart(methods_list_descriptor):
    bottom, top = 0, 100
    for data_method in methods_list_descriptor:
        plt.plot(np.arange(len(data_method['rnx'])), 100 * data_method['rnx'], label=f"{data_method['title']}:{round(data_method['score'] * 100, 3)}%")

    plt.xscale('log')
    plt.ylim(bottom, top)
    plt.legend()
    plt.show()
