

class Campeon:
    def __init__(self, codigo, nombre, partidas, poder_base):
        self.codigo = codigo
        self.nombre = nombre
        self.partidas = partidas
        self.poder_base = poder_base

    def __str__(self):
        return f"{self.codigo}{self.nombre}{self.nombre}{self.poder_base}"

    
    def poder(self):
        return self.poder_base


    