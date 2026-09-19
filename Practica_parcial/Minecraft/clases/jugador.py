class Jugador:
    def __init__(self, nickname, nivel, rango):
        self.nickname = nickname
        self.nivel = nivel
        self.rango = rango


    def __str__(self):
        return f"Nickname: {self.nickname} Nivel: {self.nivel} Rango: {self.rango}"
    