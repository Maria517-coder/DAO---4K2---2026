from abc import ABC, abstractmethod

class Empleado(ABC):
    def __init__(self, legajo, nombre, apellido, sueldoBasico):
        self.legajo = legajo
        self.nombre = nombre
        self.apellido = apellido
        self.sueldoBasico = sueldoBasico


    @abstractmethod
    def calcularSueldo(self):
        pass

class Obrero(Empleado):
    def __init__(self, legajo, nombre, apellido, sueldoBasico):
        super().__init__(legajo, nombre, apellido, sueldoBasico)
        self.dias = dias
        

class Administrativo(Empleado):
    pass

class Vendedor(Empleado):
    pass