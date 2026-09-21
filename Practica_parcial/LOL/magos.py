from campeon import Campeon

class Mago(Campeon):
    def __init__(self, codigo, nombre, partidas, poder_base, habilidades_area, prioridad_baneo):
        super().__init__(codigo, nombre, partidas, poder_base)
        self.habilidades_area = habilidades_area
        self.prioridad_baneo = prioridad_baneo

    def __str__(self):
        return f"{self.codigo} - {self.nombre} (Mago)"

    def poder(self):
        poder = self.poder_base + (self.habilidades_area * 30)
        if self.prioridad_baneo: 
            poder += 100
        return poder