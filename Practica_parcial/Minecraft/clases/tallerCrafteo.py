class Taller:
    def __init__(self):
        
        self.crafteos = []

    def __str__(self):
        return f"Nombre: {self.nombre}"

    # Métodos
    def addCrafteo(self, crafteo):
        self.crafteos.append(crafteo)

    def totalRecaudado(self):
        suma = 0.0
        for crafteo in self.crafteos:
            suma += crafteo.calcularCostoFinal()
        return suma

    def totalPorJugador(self, nickname):
        suma = 0.0
        for crafteo in self.crafteos:
            if crafteo.jugador.nickname == nickname:
                suma += crafteo.calcularCostoFinal()
        return suma

    def promedioEnRango(self, minimo, maximo):
        total = 0.0
        cantidad = 0
        for crafteo in self.crafteos:
            costo = crafteo.calcularCostoFinal()
            if minimo <= costo <= maximo:
                total += costo
                cantidad += 1

        if cantidad > 0:
            return total / cantidad
        return 0.0

    def buscarPrimeroDeJugador(self, nickname):
        for crafteo in self.crafteos:
            if crafteo.jugador.nickname == nickname:
                return crafteo
        return None

    def buscarPrimeroMayorA(self, umbral):
        for crafteo in self.crafteos:
            if crafteo.calcularCostoFinal() > umbral:
                return crafteo
        return None

    def contarPorTipo(self, tipo):
        cantidad = 0
        for crafteo in self.crafteos:
            if isinstance(crafteo, tipo):
                cantidad += 1
        return cantidad

    def crafteoMasCaro(self):
        masCaro = None
        maximo = 0.0
        for crafteo in self.crafteos:
            costo = crafteo.calcularCostoFinal()
            if masCaro is None or costo > maximo:
                masCaro = crafteo
                maximo = costo
        return masCaro