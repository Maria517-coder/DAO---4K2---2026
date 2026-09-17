from atencion import Atencion


class AtencionMedica(Atencion):

    def __init__(self, codigo, tipoDeCobro, paciente, importe):
        super().__init__(codigo, tipoDeCobro)
        self.paciente = paciente
        self.importe = importe

    @property
    def paciente(self):
        return self._paciente

    @paciente.setter
    def paciente(self, valor):
        self._paciente = valor

    @property
    def importe(self):
        return self._importe

    @importe.setter
    def importe(self, valor):
        self._importe = float(valor)

    def importeACobrar(self):
        pass