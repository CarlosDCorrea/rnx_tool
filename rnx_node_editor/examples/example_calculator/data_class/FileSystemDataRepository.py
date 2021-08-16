import scipy.io as sio
from .DataClass import Data


class FileSystemRepository:

    def load(self, path, label = "ans") -> Data:
        
        try:
            data = sio.loadmat(path)[label]
            return Data(data, path)
        except Exception as e:
            print(e)



    def save(self, X, path: str, label = "any"):

        if(label == "any"):
            sio.savemat(path, {"any": X})
        else:
            sio.savemat(path, {label: X})

