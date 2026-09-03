class Persona:
    def __init__(self, documento, nombre, apellido, edad):
        self.documento = documento
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad

# Crear una lista para almacenar las instancias de Persona
personas = []

# Solicitar al usuario la cantidad de personas a ingresar
cantidad_personas = int(input("Ingrese la cantidad de personas a registrar: "))

# Pedir datos de las personas y crear instancias de Persona
for i in range(cantidad_personas):
    print(f"Ingresando datos de la persona {i + 1}:")
    documento = input("Documento: ")
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    edad = int(input("Edad: "))
    persona = Persona(documento, nombre, apellido, edad)
    personas.append(persona)

# Mostrar el estado de las personas ingresadas
print("\nEstado de las personas ingresadas:")
for persona in personas:
    print(f"Documento: {persona.documento}")
    print(f"Nombre: {persona.nombre}")
    print(f"Apellido: {persona.apellido}")
    print(f"Edad: {persona.edad}")
    print("-" * 20)

# Encontrar y mostrar la persona de menor edad
persona_menor_edad = min(personas, key=lambda x: x.edad)
print(f"La persona de menor edad es: {persona_menor_edad.nombre} {persona_menor_edad.apellido} (Edad: {persona_menor_edad.edad})")
