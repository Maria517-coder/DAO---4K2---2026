from equipo import Equipo
from magos import Mago
from tanque import Tanque


def main():
  instancia = Equipo()

  with open("LOL.csv", "r", encoding="utf-8") as archivo:
    for linea in archivo:
      linea = linea.strip()
      if not linea:
        continue

      datos = linea.split(",")
      tipo = int(datos[0])
      codigo = int(datos[1])
      nombre = datos[2]
      poder_base = float(datos[3])  # Columna 3: poder_base (ej. 540.0)
      partidas = int(datos[4])  # Columna 4: partidas (ej. 320)

      if tipo == 1:
        habilidades_area = int(datos[5])
        prioridad_baneo = int(datos[6]) == 1
        campeon = Mago(
            codigo,
            nombre,
            partidas,
            poder_base,
            habilidades_area,
            prioridad_baneo,
        )
        instancia.agregar(campeon)

      elif tipo == 2:
        armadura = float(datos[5])
        dificultad = int(datos[6])
        campeon = Tanque(
            codigo, nombre, partidas, poder_base, armadura, dificultad
        )
        instancia.agregar(campeon)

  print(instancia.suma_poderes())
  print(instancia.cantidad_magos_elite())
  print(instancia.nombre_tanque_mas_debil())


if __name__ == "__main__":
  main()