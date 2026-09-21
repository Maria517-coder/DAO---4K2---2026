from abc import ABC, abstractmethod


class Sucursal(ABC):
    def __init__(self, numero, superficie, facturacion):
        self.numero = numero
        self.superficie = superficie
        self.facturacion = facturacion

    def __str__(self):
        return f"{self.numero} {self.tipo()}"
    
    @abstractmethod
    def resultado_comercial(self):
        pass

    @abstractmethod
    def es_rentable(self):
        pass

    @abstractmethod
    def tipo(self):
        pass
    
