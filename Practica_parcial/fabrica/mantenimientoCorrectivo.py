from mantenimiento import Mantenimiento

class Correctivo(Mantenimiento):
    def __init__(self, fecha, operario, repuestos, horas_parada, tecnico ):
        super().__init__(fecha, operario, repuestos)
        self.horas_parada = horas_parada
        self.tecnico = tecnico 


   
    def gasto_total(self):
        return self.repuestos + self.tecnico
