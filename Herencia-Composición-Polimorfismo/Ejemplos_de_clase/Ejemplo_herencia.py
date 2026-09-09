class Vehiculo():
    color = "Rojo"
    ruedas = 4

class Coche(Vehiculo):
    velocidad = 200
    cilindrada = 1700

automotor = Coche()
print("Color: ", automotor.color, "Velocidad: ", automotor.velocidad)

# Polimorfismo --> no interesa qué se va a ejecutar, sabemos que se va a ajecutar lo correcto
# Permite que diferentes objetos respondan al mismo mensaje de manera distinta
# Nos importan los metodos y comportamiento (Vuela sirve tanto para pajaro como para avión)
# Las clases abstractas nos sirven para hacer polimorfismo 
# Las clases abstractas son clases incompletas que no se pueden instanciar por sí mismas.





