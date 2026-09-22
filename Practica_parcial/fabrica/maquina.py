from mantenimientoCorrectivo import Correctivo
class Maquina:
    def __init__(self):
        self.mantenimientos = []


    def agregar_mantenimiento(self, mantenimiento):
        self.mantenimientos.append(mantenimiento)

    def suma_gastos(self):
        suma = 0
        for mantenimiento in self.mantenimientos:
            suma += mantenimiento.gasto_total()
        return suma

    def cantidad_mantenimientos_caros(self):
        cont = 0
        for mantenimiento in self.mantenimientos:
            if mantenimiento.gasto_total() > 10000:
                cont += 1
        return cont

    def rotura_mas_larga(self):
        mayor = None
        for mantenimiento in self.mantenimientos:
            if isinstance(mantenimiento, Correctivo):
                if mayor is None or mantenimiento.horas_parada > mayor.horas_parada:
                    mayor = mantenimiento
        if mayor is None:
            return None
        return f"{mayor.fecha} {mayor.operario}"

    