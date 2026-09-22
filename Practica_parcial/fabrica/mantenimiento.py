from abc import ABC, abstractmethod

class Mantenimiento(ABC):
    def __init__(self, fecha, operario, repuestos ):
        self.fecha = fecha
        self.operario = operario
        self.repuestos = repuestos

    @abstractmethod
    def gasto_total(self):
        pass
