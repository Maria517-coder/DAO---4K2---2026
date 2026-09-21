from campeon import Campeon

class Tanque(Campeon):
    def __init__(self, codigo, nombre, partidas, poder_base, armadura, dificultad):
        super().__init__(codigo, nombre, partidas, poder_base)
        self.armadura = armadura
        self.dificultad = dificultad

    def __str__(self):
        return f"{self.codigo} - {self.nombre} (Tanque)"

    def poder(self):
        poder = self.poder_base + self.armadura
        if self.dificultad < 4:
            poder += 20
        return poder