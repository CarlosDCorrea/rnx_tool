from scipy.io import  loadmat, savemat
from .DataClass import Data
from pandas import read_csv, read_excel, DataFrame


class FileSystemRepository:

    def load(self, path, label = "ans") -> Data:

        extention = self.getExtention(path)
        data = None
        try:
            if extention == "mat":
                data = loadmat(path)[label]
                data = DataFrame(data, columns=["component1", "component2", "component3"])

            if extention == "csv":
                data = read_csv(path)

            if extention == "xlsx":
                data = read_excel(path)

            return data


        except Exception as e:
            print(e)

    def save(self, X, path: str, label = "any"):

        if(label == "any"):
            savemat(path, {"any": X})
        else:
            savemat(path, {label: X})

    def getExtention(self, path:str):
        return path.split(".")[-1]
