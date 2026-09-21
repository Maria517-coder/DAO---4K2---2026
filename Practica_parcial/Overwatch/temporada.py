# from partida import Partida

class Temporada:
    def __init__(self, nombre):
        self.nombre = nombre
        self.partidas = []

    def addPartida(self, partida):
        self.partidas.append(partida)

    def experienciaTotal(self):
        suma = 0
        for partida in self.partidas:
            suma += partida.calcularExperiencia()
        return suma

    def experienciaPorJugador(self, battletag):
        suma = 0
        for partida in self.partidas:
            if partida.jugador.battletag == battletag:
                suma += partida.calcularExperiencia()
        return suma

    def promedioEnRango(self, minimo, maximo):
        prom = 0
        suma = 0
        cont = 0
        for partida in self.partidas:
            if minimo < partida.calcularExperiencia() < maximo:
                suma += partida.calcularExperiencia()
                cont += 1
        if cont > 0:
            prom = suma / cont
            return prom
        return prom

    def buscarPrimeraDeJugador(self, battletag):
        for partida in self.partidas:
            if partida.jugador.battletag == battletag:
                return partida
        return None

    def buscarPrimeraMayorA(self, umbral):
        for partida in self.partidas:
            if partida.calcularExperiencia() > umbral:
                return partida
        return None

    def contarPorTipo(self, tipo):
        cont = 0
        for partida in self.partidas:
            if isinstance(partida, tipo):
                cont += 1
        return cont

    def partidaMasLarga(self):
        mas_larga = None
        for partida in self.partidas:
            if mas_larga is None or partida.duracionMinutos > mas_larga.duracionMinutos:
                mas_larga = partida
        return mas_larga