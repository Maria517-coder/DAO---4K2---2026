class Jugador:
    def __init__(self, battletag, nivel, rol ):
        self.battletag = battletag
        self.nivel = nivel
        self.rol = rol

    def __str__(self):
        return f"{self.battletag}{self.nivel}{self.rol}"

    