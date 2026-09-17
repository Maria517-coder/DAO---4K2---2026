class Paciente:
    def __init__(self, nombre, sintoma, habitual):
        self.nombre = nombre
        self.sintoma = sintoma
        self.habitual = habitual

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self.nombre = str(valor)

    @property
    def sintoma(self):
        return self. sintoma

    sintoma.setter
    def sintoma(self, valor):
        self.sintoma = str(valor)

    @property
    def habitual(self):
        return self.habitual

    habitual.setter
    def habitual(self, valor):
        self.habitual = bool(valor)

