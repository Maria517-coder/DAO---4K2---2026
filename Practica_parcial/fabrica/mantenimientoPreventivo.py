from mantenimiento import Mantenimiento

class Preventivo(Mantenimiento):
    def __init__(self, fecha, operario, repuestos, resultado, insumos ):
        super().__init__(fecha, operario, repuestos)
        self.resultado = resultado
        self.insumos = insumos


   
    def gasto_total(self):
        return self.repuestos + self.insumos
