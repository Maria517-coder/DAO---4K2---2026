from abc import ABC, abstractmethod

# Atencion(ABC) y el @abstractmethod bloquean la creación directa de la clase

# @property son getters
# @atributo.setter son setters


class Atencion:
    def __init__(self, codigo, tipoDeCobro):
        self.codigo = codigo
        self.tipoDeCobro = tipoDeCobro

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        self._codigo = int(valor)

    @property
    def tipoDeCobro(self):
        return self._tipoDeCobro

    @tipoDeCobro.setters
    def tipoDeCobro(self, valor):
        self.tipoDeCobro = int(valor)

    @abstractmethod
    def importeACobrar(self):
        pass

    

