from crafteo import Crafteo

class CrafteoArma(Crafteo):
    def __init__(self, idCrafteo, item, costoBase, cantidad, jugador, danio, encantada):
        super().__init__(idCrafteo, item, costoBase, cantidad, jugador)
        self.danio = danio
        self.encantada = encantada

    def __str__(self):
        return f"Daño: {self.danio}, encatada: {self.encantada}"

    # Métdos

    def calcularCostoFinal(self):
        subtotal = 0
        subtotal = (self.costoBase + self.danio * 1.5) * self.cantidad
        if self.encantada == True:
            subtotal = subtotal * 1.25

        if self.jugador.rango == "Leyenda":
            subtotal = subtotal * 0.8

        if self.jugador.rango == "Veterano":
            subtotal = subtotal * 0.9

        return subtotal


def principal():
    ins1 = CrafteoArma(112, "Pocion de curacion" ,12.0,2, "GolemBuilder" ,2,"no")
    print(ins1)

if __name__ == "__main__":
    principal()