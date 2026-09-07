class Habitacion:
    def __init__(self, numero, cantidad_personas, precio_noche, estado_ocupacion):
        self.numero = numero
        self.cantidad_personas = cantidad_personas
        self.precio_noche = precio_noche
        self.estado_ocupacion = estado_ocupacion

    def __str__(self):
        return f"Numero: {self.numero} Cantidad de personas: {self.cantidad_personas} Precio por noche: {self.precio_noche} Estado de ocupacion: {self.estado_ocupacion}"

    def ocupar(self):
        if self.estado_ocupacion == True:
            return "Esta habitacion ya se encuentra ocupada"
        else:
            self.estado_ocupacion = True
            return "Habitacion ocupada correctamente!!"

def principal():
    habitacion_1 = Habitacion(101, 2, 1500, False)
    print(habitacion_1)
    print(habitacion_1.ocupar())
    print(habitacion_1)

if "__main__" == __name__:
    principal()