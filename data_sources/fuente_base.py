from abc import ABC, abstractmethod


class FuenteDatos(ABC):

    @abstractmethod
    def conectar(self):
        pass

    @abstractmethod
    def desconectar(self):
        pass

    @abstractmethod
    def esta_disponible(self):
        pass