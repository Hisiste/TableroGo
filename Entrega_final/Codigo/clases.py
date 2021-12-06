import numpy as np

FREE  = -1
BLACK = False   # 0
WHITE = True    # 1

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
                        fichasPorInvestigar.append(vecino)
                    elif tablero[vecino] == FREE:
                        self.__puntosDeLibertad.add(vecino)

            fichasInvestigadas.add((y, x))

    def numLibertades(self):
        return len(self.__puntosDeLibertad)

    def get_fichasEnCluster(self):
        return [(x, y) for y, x in self.__fichasDelCluster]

    def fichaEnLibertad(self, x: int, y: int):
        return (y, x) in self.__puntosDeLibertad


class Tablero_Go:
    """Todo con respecto a un tablero de Go
    Se guardarán tableros, se podrán realizar movimientos y se asegurará de que
    todas las reglas de Go se cumplan.
    """

    def __init__(self, size: int):
        self._tamano   = size
        self._tableros = np.full((4, self._tamano, self._tamano), FREE)
        # tableros[0] -> futuro 1 movimiento.
        # tableros[1] -> presente.
        # tableros[2] -> pasado 1 movimiento.
        # tableros[3] -> pasado 2 movimientos.
        self._listaClusters = np.full((2, self._tamano**2), None)
        # listaClusters[0] -> futuro 1 movimiento.
        # listaClusters[1] -> presente.
        self._clustTablero  = np.full((self._tamano, self._tamano), FREE)
        self.__porAgregar     = []
        self.__porEliminar    = []

    def __borrarClusterIdx(self, idx: int):
        """Borrar el cluster de índice `idx` del tablero del futuro.
        El objeto `Cluster` *no* se eliminará, pues estamos hablando del posible
        futuro. Es posible que al final no se necesite borrar, por lo que lo
        único que se hará será guardarlo en una lista. Esto para poder borrarlo
        en caso de ser necesario.
        """
        self.__porEliminar.append(self._listaClusters[0][idx])
        self._listaClusters[0][idx] = None

    def __actDespuesDeBorrar(self):
        j = 1

        for i in range(self._tamano**2):
            if self._listaClusters[0][i] is not None:
                j += 1
                continue

            while j < self._tamano**2 and self._listaClusters[0][j] is None:
                j += 1

            if j >= self._tamano**2:
                break

            self._listaClusters[0][i], self._listaClusters[0][j] = self._listaClusters[0][j], self._listaClusters[0][i]
            j += 1

    def __agregarCluster(self, clust: Cluster):
        """Añadir un nuevo cluster a la lista.
        Se buscará el primer espacio vacío en la lista de clusters para añadir
        el nuevo cluster. Se regresa el índice del nuevo cluster.
        """
        self.__porAgregar.append(clust)

        for i in range(self._tamano**2):
            if self._listaClusters[0][i] is None:
                self._listaClusters[0][i] = clust
                return i

        raise AssertionError("No hay suficientes espacios para guardar clusters.")

    def __prepararFuturo(self):
        """Preparando el tablero del futuro y lo demás.
        Copiaremos el tablero del presente al futuro. Olvidaremos los clusters
        que se iban a eliminar y eliminaremos los que se iban a agregar. Por
        último, copiaremos la lista de clusters a la del futuro.
        """
        if len(self.__porAgregar) == 0:
            return

        for elim in self.__porAgregar:
            del elim
        self.__porAgregar  = []
        self.__porEliminar = []

        self._tableros[0]      = self._tableros[1].copy()
        self._listaClusters[0] = self._listaClusters[1].copy()

    def __moverTableroAFuturo(self):
        """Moviendo el tablero 1 movimiento al futuro.
        Se actualizarán los tableros del presente y pasado a un movimiento en
        futuro. El tablero de 2 movimientos al pasado será eliminado y se
        eliminarán los clusters del tablero del presente.
        """
        self._tableros[3]      = self._tableros[2].copy()
        self._tableros[2]      = self._tableros[1].copy()
        self._tableros[1]      = self._tableros[0].copy()
        self._listaClusters[1] = self._listaClusters[0].copy()

        for elim in self.__porEliminar:
            del elim
        self.__porAgregar  = []
        self.__porEliminar = []

        self._clustTablero  = np.full((self._tamano, self._tamano), FREE)
        for idx, cluster in enumerate(self._listaClusters[1]):
            if cluster == None:
                break

            for x, y in cluster.get_fichasEnCluster():
                self._clustTablero[y, x] = idx


    def esEspacioValido(self, x: int, y: int, color: bool):
        if self._tableros[1][(y, x)] != FREE:
            return False

        self.__prepararFuturo()
        self._tableros[0][y, x] = color
        nuevoCluster = Cluster(x, y, color, self._tableros[0])
        self.__agregarCluster(nuevoCluster)

        clustVecinos = set()
        for vecino in dameVecinos(y, x, self._tableros[0].shape):
            if self._clustTablero[vecino] != FREE:
                clustVecinos.add((self._clustTablero[vecino], self._listaClusters[0][self._clustTablero[vecino]]))

        if len(clustVecinos) == 0:
            return True

        for idx, clust in list(clustVecinos):
            if clust.color == color:
                self.__borrarClusterIdx(idx)
        clustVecinos = [x for x in clustVecinos if x[1].color != color]

        for idx, clust in clustVecinos:
            clust.actualizarCluster(self._tableros[0])
            if clust.numLibertades == 0:
                for x, y in clust.get_fichasEnCluster():
                    self._tableros[0][y, x] = FREE
                self.__borrarClusterIdx(idx)

        self.__actDespuesDeBorrar()
        nuevoCluster.actualizarCluster(self._tableros[0])

        if np.array_equal(self._tableros[0], self._tableros[2]):
            return False
        elif nuevoCluster.numLibertades() == 0:
            return False
        else:
            return True

    def ponerFicha(self):
        """Poner una ficha de color `color` en el espacio `(y, x)`.
        Suponemos que el lugar ya es válido y no se checará.
        """
        self.__moverTableroAFuturo()

    def calcularPuntaje(self):
        pass

    def dibujarTablero(self):
        return [(x.color, x.get_fichasEnCluster()) for x in
                self._listaClusters[1] if x is not None]


