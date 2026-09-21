from partida import Partida
from jugador import Jugador

class PartidaRapida(Partida):
    def __init__(self, idPartida, mapa, duracionMinutos, eliminaciones, victoria, jugador, eventoEspecial):
        super().__init__(idPartida, mapa, duracionMinutos, eliminaciones, victoria, jugador)
        self.eventoEspecial = eventoEspecial 

    def __str__(self):
            return f"{self.idPartida} : {self.mapa} : {self.duracionMinutos} : {self.eliminaciones} : {self.victoria} : {self.jugador} : {self.eventoEspecial}"


    def calcularExperiencia(self):
            xp = self.duracionMinutos * 10 + self.eliminaciones * 5
            if self.victoria:
                  xp = xp + 100
            if self.eventoEspecial:
                  xp = xp * 1.25
            if self.jugador.nivel < 50:
                  xp = xp * 1.5
            return xp
        