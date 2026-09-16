from atencion import *

class AtencionMedica(Atencion):
    def __init__(self, codigo, tipo_de_cobro, paciente, importe):
        # Llamo a super con los atributos del padre
        super().__init__(codigo, tipo_de_cobro)
        self.importe = importe
        self.paciente = paciente