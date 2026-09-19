from abc import ABC, abstractmethod

class Crafteo(ABC):
    def __init__(self, idCrafteo, item, costoBase, cantidad, jugador):
        self.idCrafteo = idCrafteo
        self.item = item
        self.costoBase = costoBase
        self.cantidad = cantidad
        self.jugador = jugador

    def __str__(self):
        return f"id Crafteo: {self.idCrafteo}{self.item}{self.costoBase}{self.cantidad}{self.jugador}"

    
    @abstractmethod
    def calcularCostoFinal(self):
        pass