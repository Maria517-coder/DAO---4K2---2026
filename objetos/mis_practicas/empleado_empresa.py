class Empleado:
    def __init__(self, legajo, nombre, sueldo, antiguedad):
        self.legajo = legajo
        self.nombre = nombre
        self.sueldo = sueldo
        self.antiguedad = antiguedad

    def __str__(self):
        return f"Legajo : {self.legajo} Nombre: {self.nombre} Sueldo: {self.sueldo} Antiguedad: {self.antiguedad}"

    def aumentar_sueldo(self, porcentaje):
        self.sueldo = self.sueldo + (self.sueldo * porcentaje / 100)
        print(f"El sueldo del empleado {self.nombre} ha sido aumentado a {self.sueldo}")

    def es_antiguo(self):
        if self.antiguedad >= 10:
            return True
        else:
            return False

def principal():
    empleado_1 = Empleado(123, "Juan Perez", 50000, 12)
    print(empleado_1)
    empleado_1.aumentar_sueldo(10)
    print(empleado_1)
    if empleado_1.es_antiguo():
        print(f"El empleado {empleado_1.nombre} es antiguo")

if "__main__" == __name__:
    principal()