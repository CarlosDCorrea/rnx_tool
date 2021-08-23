import matplotlib.pyplot as plt
import numpy as np
import random

def line_chart(methods_list_descriptor):

    markers = ['.', '>', 'o']
    bottom, top = 0, 100
    for data_method in methods_list_descriptor:
        plt.plot(np.arange(len(data_method['rnx'])), 100 * data_method['rnx'],
                 label=f"{data_method['title']}:{round(data_method['score'] * 100, 3)}%",
                 marker=random.choice(markers),
                 markevery=0.1)

    plt.xscale('log')
    plt.ylim(bottom, top)
    plt.xlabel("K")
    plt.ylabel("100RNX (K)")

    plt.legend(loc='lower center', shadow=True, fontsize='x-large')
    plt.show()
