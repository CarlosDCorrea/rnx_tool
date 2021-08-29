from scipy.io import loadmat, savemat
from .DataClass import Data
from pandas import read_csv, read_excel, DataFrame
import os


class FileSystemRepository:

    def load(self, path, separator=None) -> Data:

        extention = os.path.splitext(path)[1]
        data = None
        try:
            if extention == ".mat":
                raw_data = loadmat(path)
                data_key = list(raw_data.keys())[-1]
                data = raw_data[data_key]
                dimensions = data.shape[1]
                cols = self.column_generator(dimensions)
                data = DataFrame(data, columns=cols)

            if extention == ".csv":
                data = read_csv(path, sep=separator)

            if extention == ".xlsx":
                data = read_excel(path)

            return data

        except Exception as e:
            print(e)

    def save(self, X, path: str, label = "any"):

        if(label == "any"):
            savemat(path, {"any": X})
        else:
            savemat(path, {label: X})

    def column_generator(self, d):
        return ['component' + str(i) for i in range(1, d + 1)]
