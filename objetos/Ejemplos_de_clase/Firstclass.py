class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def saludar(self):
        print(f"Hola, mi nombre es {self.nombre} y tengo {self.edad} años.")

    def cumpleanios(self):
        self.edad += 1
        print(f"Feliz cumpleaños, ahora tengo {self.edad} años!")

# Crear una instancia de la clase Persona
persona1 = Persona("Juan", 30)
persona1.edad=-50
# Acceder a las propiedades y métodos de la instancia
print(persona1.nombre)  # Acceder a la propiedad nombre
print(persona1.edad)    # Acceder a la propiedad edad
persona1.saludar()      # Llamar al método saludar
persona1.cumpleanios()  # Llamar al método cumpleanios
