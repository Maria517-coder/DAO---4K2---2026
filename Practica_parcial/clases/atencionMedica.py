from atencion import Atencion


class AtencionMedica(Atencion):

    def __init__(self, codigo, tipoDeCobro, paciente, importe):
        super().__init__(codigo, tipoDeCobro)
        self.paciente = paciente
        monto = importe

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
        monto = self.importe
        if self.paciente.habitual == True:
            monto = monto * 0.75
        if self.tipoDeCobro == 1:
            monto = monto * 0.90
        if self.tipoDeCobro == 2:
            monto = monto * 1.20

        return monto

    