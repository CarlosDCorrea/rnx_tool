from typing import Any
import numpy as np
from numpy import ndarray
from timeit import default_timer as timer
from rnx_node_editor.utils import dump_exception
from pandas import DataFrame


DEBUG = False


class CorankingException(Exception):
    def __init__(self, message, *args):
        super(CorankingException, self).__init__(message, *args)


class NX_TrusionException(Exception):
    def __init__(self, message, *args):
        super(NX_TrusionException, self).__init__(message, *args)


class Pairwisedistances(Exception):
    def __init__(self, message, *args):
        super(Pairwisedistances, self).__init__(message, *args)


class ScoreRnx:
    def __init__(self, data:ndarray, method:ndarray) -> None:
        self.__data = data
        self.__method = method
        self.__score = 0
        self.__curve = Any

    def run(self):
        try:
            [Ravg, R_NX] = self.nx_scores(self.__data, self.__method)
            self.__score = Ravg
            self.__curve = R_NX

        except Exception as e:
            print(e)
            #lanzar una excepcion

    def get_rnx(self):
        return [self.__score, self.__curve]

    def nx_scores(self, HD: np.ndarray, LD: np.ndarray):
        try:
            nbr = len(HD)
            # Crear matrices de distancias para datos en alta y baja dimension
            start = timer()
            DX = self.pairwisedistances(HD)
            if DEBUG:
                print(f"DX process =>, {timer() - start:0.4f} sec")
            del start

            start = timer()
            DYt = self.pairwisedistances(LD)
            if DEBUG:
                print(f"DYt process =>, {timer() - start:0.4f} sec")
            del start
            # Crear la matriz de coranking con las matrices de distancias
            #   Nota: Tener encuenta que , coranking(DX, DYt) es diferente a    coranking(DYt, DX)

            start = timer()
            co = self.coranking(DX, DYt)
            if DEBUG:
                print(f"CO process =>, {timer() - start:0.4f} sec")
            del start

            start = timer()
            [n, x, p, b] = self.nx_trusion(co)
            # n => intrusiones, x => extrusiones, b => base aleatoria, p => tasa de rangos perfectamente conservados
            print(f"TRUSION process =>, {timer() - start:0.4f} sec")
            del start

            Q_NX = n + x + p  # Calidad general de incrustracion, varia entre 0-1

            B_NX = x - n  # Comportamiento
            LCMC = Q_NX - b  # Meta  criterio de continuidad local
            R_NX = LCMC[0: LCMC.shape[0] - 1] / (1 - b[0: b.shape[0] - 1])  # Convertir q_nx a r_nx

            wgh = np.divide(1, np.arange(1, nbr + 1))  # 1 / np.arange(1, nbr + 1)
            wgh = np.sum(np.divide(wgh, np.sum(wgh)))  # wgh / np.sum(wgh)
            wgh = np.divide(1, np.arange(1, nbr - 1))  # 1 / np.arange(1, nbr - 1)
            wgh = np.divide(wgh, sum(wgh))  # wgh / sum(wgh)
            Ravg = np.sum(wgh * R_NX)

            return [Ravg, R_NX]

        except Exception as e:
            print(e)
            raise e

    def pairwisedistances(self, X: np.ndarray):
        X = np.array(X, dtype=np.float64)

        g = np.dot(X, np.transpose(X))
        print("G =>", np.sum(np.sum(g)))

        di = np.diag(g)
        print("DI =>", np.sum(np.sum(di)))
        d = np.transpose(np.subtract(di, g ))
        print("D =>", np.sum(np.sum(d)))
        matrix_squared = (d + np.transpose(d))
        print("MS =>", np.sum(np.sum(matrix_squared)))
        try:

            result = np.sqrt(abs(matrix_squared))

            return result
        except Exception as e:
            dump_exception(e)

    def coranking(self, HD: np.ndarray, LD: np.ndarray):
        try:
            if HD.size != LD.size:
                raise CorankingException("matrices hdpd and ldpd do not have the same sizes")

            nbr = HD.shape[0]
            sss = HD.shape[1]

            ndx1 = np.transpose(np.argsort(HD+1, axis=1))
            ndx2 = np.transpose(np.argsort(LD+1, axis=1))

            ndx1 = ndx1 + 1
            ndx2 = ndx2 + 1

            ndx4 = np.zeros((nbr+1, sss+1), dtype=np.uint32)
            start = timer()

            nbr_range = range(nbr)

            for j in range(sss):
                ndx4[ndx2[nbr_range, j], j] = nbr_range

            ndx4 = ndx4 + 1

            print(f"FIRST O(N^2) process =>, {timer() - start:0.4f} sec")

            del ndx2

            c = np.zeros((nbr+1, sss+1), dtype=np.uint32)

            start = timer()

            for j in range(sss):
                h = ndx4[ndx1[nbr_range, j], j]
                c[nbr_range, h] = c[nbr_range, h] + 1

            print(f"SECOND O(N^2) process =>, {timer() - start:0.4f} sec")
            del ndx1, ndx4

            c = np.delete(c, 0, axis=0)
            c = np.delete(c, 0, axis=1)
            c = np.delete(c,0, axis = 1)
            c = np.delete(c, -1, axis = 0)
            return c

        except Exception as e:
            print(e)
            raise CorankingException(e)

    def first(self, ):
        pass

    def nx_trusion(self, c: np.ndarray):
        try:
            size = c.shape
            print(size)
            if size[0] != size[1]:
                return
            nmo = size[0]
            sss = np.sum(c, axis=1)
            sss = sss[0]

            v1 = np.arange(1, nmo + 1)
            v2 = np.dot(sss, v1)

            n = np.zeros(nmo)

            x = np.zeros(nmo)

            p = np.cumsum(np.diag(c)) / v2

            b = v1 / nmo

            v3 = []

            for k in range(1, nmo):
                v3.append(k - 1)
                n[k] = np.sum(c[k, v3])
                x[k] = np.sum(c[v3, k])

            n = np.cumsum(n) / v2
            x = np.cumsum(x) / v2

            return [n, x, p, b]

        except Exception as e:
            print(e)
            raise NX_TrusionException(e)
