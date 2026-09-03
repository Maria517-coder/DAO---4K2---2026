class Persona:
    def __init__(self, nombre, edad):
        self._nombre = nombre  # Propiedad privada con guion bajo
        self._edad = edad

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        if isinstance(nuevo_nombre, str):
            self._nombre = nuevo_nombre
        else:
            raise ValueError("El nombre debe ser una cadena de caracteres")

    @property
    def edad(self):
        return self._edad

    @edad.setter
    def edad(self, nueva_edad):
        if nueva_edad >= 0:
            self._edad = nueva_edad
        else:
            raise ValueError("La edad debe ser un número positivo")

# Crear una instancia de la clase Persona
persona = Persona("Juan", 30)

# Obtener el valor de la propiedad nombre
print(persona.nombre)

# Establecer un nuevo valor para la propiedad nombre
persona.nombre = "Carlos"
print(persona.nombre)

# Intentar establecer un valor no válido para la propiedad nombre
try:
    persona.nombre = 123  # Esto generará una excepción
except ValueError as e:
    print(e)
