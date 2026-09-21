class Empresa:
    def __init__(self):
        self.sucursales = []

    def agregar_sucursal(self, sucursal):
        self.sucursales.append(sucursal)

    def suma_ganancia(self):
        suma = 0
        for sucursal in self.sucursales:
            suma += sucursal.resultado_comercial()
        return suma

    def cantidad_no_rentables(self):
        cont = 0
        for sucursal in self.sucursales:
            if sucursal.es_rentable() is False:
                cont += 1
        return cont

    def local_mas_rentable(self):
        mayor = None
        for sucursal in self.sucursales:
            if mayor is None or sucursal.indice() > mayor.indice():
                mayor = sucursal
        return mayor


