from partida import Partida

class PartidaCompetitiva(Partida):
    def __init__(self, idPartida, mapa, duracionMinutos, eliminaciones, victoria, jugador, racha):
        super().__init__(idPartida, mapa, duracionMinutos, eliminaciones, victoria, jugador)
        self.racha = racha 

    def __str__(self):
            return f"{self.idPartida} : {self.mapa} : {self.duracionMinutos} : {self.eliminaciones} : {self.victoria} : {self.jugador} : {self.racha}"

    def calcularExperiencia(self):
            xp = self.duracionMinutos * 15 + self.eliminaciones * 8
            if self.victoria:
                  xp = xp * 1.5
            else: 
                  xp = xp * 0.5

            if self.racha <= 5:
                  xp = xp * (1 + 0.10 * self.racha)
            else:
                  xp = xp * (1 + 0.10 * 5)

            if self.jugador.rol == "Tanque":
                  xp = xp + 40

            return xp 

    

        
    