from abc import ABC, abstractmethod

class Partida(ABC):
    def __init__(self, idPartida, mapa, duracionMinutos, eliminaciones, victoria, jugador):
        self.idPartida = idPartida
        self.mapa = mapa
        self.duracionMinutos = duracionMinutos
        self.eliminaciones = eliminaciones
        self.victoria = victoria
        self.jugador = jugador

    def __str__(self):
        return f"{self.idPartida}{self.mapa}{self.duracionMinutos}{self.eliminaciones}{self.victoria}{self.jugador}"

    @abstractmethod
    def calcularExperiencia(self):
        pass

    