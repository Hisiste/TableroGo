import numpy as np

FREE  = -1
BLACK = False
WHITE = True

def dameVecinos(y: int, x: int, tab_shape: tuple):
    if x > 0:
        yield (y    , x - 1)
    if y > 0:
        yield (y - 1, x    )

    if x < tab_shape[1] - 1:
        yield (y    , x + 1)
    if y < tab_shape[0] - 1:
        yield (y + 1, x    )

class Cluster:
    """Los grupos de fichas de Go.
    Cada grupo de fichas tendrá métodos que nos facilitará el seguimiento de las
    reglas de Go.
    """
    def __init__(self, x: int, y: int, color: bool, tablero: np.ndarray):
        self.color = color

        self.__fichasDelCluster = set()
        self.__fichasDelCluster.add((y, x))

        self.__puntosDeLibertad = set()
        self.actualizarCluster(tablero)

    def actualizarCluster(self, tablero: np.ndarray):
        ficha = next(iter(self.__fichasDelCluster))

        fichasPorInvestigar = list()
        fichasPorInvestigar.append(ficha)
        fichasInvestigadas  = set()
        fichasInvestigadas.add(ficha)

        while fichasPorInvestigar:
            y, x = fichasPorInvestigar.pop()

            for vecino in dameVecinos(y, x, tablero.shape):
                if vecino not in fichasInvestigadas:
                    if tablero[vecino] == self.color:
                        self.__fichasDelCluster.add(vecino)
                        fichasInvestigadas.add(vecino)
                        fichasPorInvestigar.append(vecino)
                    elif tablero[vecino] == FREE:
                        self.__puntosDeLibertad.add(vecino)
                        fichasInvestigadas.add(vecino)

    def numLibertades(self):
        return len(self.__puntosDeLibertad)

    def get_fichasEnCluster(self):
        return list(self.__fichasDelCluster)

    def fichaEnLibertad(self, x: int, y: int):
        return (y, x) in self.__puntosDeLibertad


class Tablero_Go:
    """Todo con respecto a un tablero de Go
    Se guardarán tableros, se podrán realizar movimientos y se asegurará de que
    todas las reglas de Go se cumplan.
    """

    def __init__(self):
        self._tamano   = 0
        self._tableros = np.full((4, self._tamano, self._tamano), FREE)
        # tableros[0] -> futuro 1 movimiento
        # tableros[1] -> presente
        # tableros[2] -> pasado 1 movimiento
        # tableros[3] -> pasado 2 movimientos
        self._listaClusters = np.full(self._tamano**2, None)
        self._clustTablero  = np.full((self._tamano, self._tamano), FREE)

    def esEspacioValido(self, x: int, y: int, color: bool):
        if self._tableros[1][(y, x)] != FREE:
            return False
        
        for posibClust in self._listaClusters:
            if posibClust == None:
                continue
        # TODO: Continuar con la validación.

    def ponerFicha(self, x: int, y: int, color: bool):
        pass

    def calcularPuntaje(self):
        pass

    def dibujarTablero(self):
        pass


