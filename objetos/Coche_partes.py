class Motor:
    def arrancar(self):
        print("Motor arrancado")

class Rueda:
    def girar(self):
        print("Rueda girando")

class Coche:
    def __init__(self):
        self.motor = Motor()  # Composición: el coche "tiene un" motor
        self.ruedas = [Rueda() for _ in range(4)]  # Composición: el coche "tiene cuatro" ruedas

    def conducir(self):
        self.motor.arrancar()
        for rueda in self.ruedas:
            rueda.girar()
