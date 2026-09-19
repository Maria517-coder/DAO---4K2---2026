from crafteo import Crafteo
# importo esto?
from jugador import Jugador

class CrafteoPocion(Crafteo):
    def __init__(self, idCrafteo, item, costoBase, cantidad, jugador, potencia, splash):
        super().__init__(idCrafteo, item, costoBase, cantidad, jugador)
        self.potencia = potencia
        self.splash = splash

    def __str__(self):
        return f"Daño: {self.danio}, encatada: {self.encantada}"


    # Métdos
    
    def calcularCostoFinal(self):
        subtotal = 0
        subtotal = self.costoBase * self.potencia * self.cantidad
        if self.splash == True:
            subtotal = subtotal + 15 * self.cantidad

        if self.jugador.nivel >= 30:
            subtotal = subtotal * 0.9

        return subtotal

    

        
            