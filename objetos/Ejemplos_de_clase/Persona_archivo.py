import csv

class Persona:
    def __init__(self, documento, nombre, apellido, edad):
        self.documento = documento
        self.nombre = nombre
        self.apellido = apellido
        self.edad = int(edad)

# Crear un diccionario para almacenar las instancias de Persona indexadas por documento
personas_dict = {}

# Leer el archivo personas.csv y crear instancias de Persona
with open('personas.csv', 'r') as archivo_csv:
    lector = csv.reader(archivo_csv)
    for linea in lector:
        documento, nombre, apellido, edad = linea
        persona = Persona(documento, nombre, apellido, edad)
        personas_dict[documento] = persona

# Informe 1: Cantidad de personas cargadas
cantidad_personas = len(personas_dict)
print(f"Cantidad de personas cargadas: {cantidad_personas}")

# Informe 2: Cantidad de personas mayores de edad
mayores_de_edad = [persona for persona in personas_dict.values() if persona.edad >= 18]
cantidad_mayores_de_edad = len(mayores_de_edad)
print(f"Cantidad de personas mayores de edad: {cantidad_mayores_de_edad}")

# Informe 3: Listado de nombres y apellidos de personas cuyo apellido empiece en vocal
apellidos_con_vocal = [persona for persona in personas_dict.values() if persona.apellido[0].lower() in 'aeiou']
print("Personas cuyo apellido empieza en vocal:")
for persona in apellidos_con_vocal:
    print(f"{persona.nombre} {persona.apellido}")

# Informe 4: Cantidad de personas por cada apellido
apellidos = [persona.apellido for persona in personas_dict.values()]
cantidad_por_apellido = {apellido: apellidos.count(apellido) for apellido in set(apellidos)}
print("Cantidad de personas por cada apellido:")
for apellido, cantidad in cantidad_por_apellido.items():
    print(f"{apellido}: {cantidad}")
