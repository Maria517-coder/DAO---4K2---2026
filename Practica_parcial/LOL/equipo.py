from magos import Mago
from tanque import Tanque

class Equipo:
    def __init__(self):
        self.campeones = []

    def agregar(self, campeon):
        self.campeones.append(campeon)

    def suma_poderes(self):
        return sum(campeon.poder() for campeon in self.campeones)

    def cantidad_magos_elite(self):
        contador = 0
        for campeon in self.campeones:
            if isinstance(campeon, Mago):
                # Usamos habilidades_area coherente con el test y el constructor
                if campeon.partidas > 150 and campeon.habilidades_area > 2 and campeon.prioridad_baneo:
                    contador += 1
        return contador

    def nombre_tanque_mas_debil(self):
        tanques = [c for c in self.campeones if isinstance(c, Tanque)]
        if not tanques:
            return None
        
        # Obtenemos el tanque con menor poder usando min() con key lambda
        tanque_debil = min(tanques, key=lambda t: t.poder())
        return tanque_debil.nombre