from crafteoPocion import CrafteoPocion
from crafteoArma import CrafteoArma
from tallerCrafteo import Taller
from jugador import Jugador


def main():
    # ----------------------------------------------------
    # 1. Carga de jugadores desde jugadores.csv
    # ----------------------------------------------------
    jugadores = {}
    archivo_jugadores = open("jugadores.csv", "r", encoding="utf-8")
    archivo_jugadores.readline()  # Salteo la cabecera (nickname,nivel,rango)

    for linea in archivo_jugadores:
        linea = linea.strip()
        if not linea:
            continue
        datos = linea.split(",")
        nickname = datos[0]
        nivel = int(datos[1])
        rango = datos[2]
        
        # Guardamos el objeto Jugador real indexado por su nickname
        jugadores[nickname] = Jugador(nickname, nivel, rango)

    archivo_jugadores.close()

    # ----------------------------------------------------
    # 2. Carga de crafteos desde crafteos.csv
    # ----------------------------------------------------
    instancia = Taller()  
    archivo = open("crafteos.csv", "r", encoding="utf-8")
    archivo.readline()  # Salteo la cabecera

    for linea in archivo:
        linea = linea.strip()
        if not linea:
            continue

        datos = linea.split(",")
        tipo = int(datos[0])
        idCrafteo = int(datos[1])
        item = datos[2]
        costoBase = float(datos[3])
        cantidad = int(datos[4])
        nickname = datos[5]

        # Obtenemos el objeto Jugador instanciado en el paso 1
        jugador_obj = jugadores[nickname]

        if tipo == 1:
            danio = int(datos[6])
            # Comparamos con "si" para obtener True o False directamente
            encantada = datos[7].strip().lower() == "si"
            crafteo = CrafteoArma(idCrafteo, item, costoBase, cantidad, jugador_obj, danio, encantada)
            instancia.addCrafteo(crafteo)

        elif tipo == 2:
            potencia = int(datos[6])
            # Comparamos con "si" para obtener True o False directamente
            splash = datos[7].strip().lower() == "si"
            crafteo = CrafteoPocion(idCrafteo, item, costoBase, cantidad, jugador_obj, potencia, splash)
            instancia.addCrafteo(crafteo)

    archivo.close()

    # ----------------------------------------------------
    # 3. Reportes y pruebas
    # ----------------------------------------------------
    print(f"Total recaudado: {instancia.totalRecaudado()}")
    print(f"Total de Steve_99: {instancia.totalPorJugador('Steve_99')}")
    print(f"Promedio en rango [100, 200]: {instancia.promedioEnRango(100, 200)}")
    
    primer_crafteo = instancia.buscarPrimeroDeJugador("Steve_99")
    print(f"Primer crafteo de Steve_99: {primer_crafteo.item if primer_crafteo else None}")
    
    crafteo_mayor = instancia.buscarPrimeroMayorA(200)
    print(f"Primer crafteo mayor a 200: {crafteo_mayor.item if crafteo_mayor else None}")
    
    print(f"Cantidad de armas: {instancia.contarPorTipo(CrafteoArma)}")
    
    mas_caro = instancia.crafteoMasCaro()
    print(f"Crafteo más caro: {mas_caro.item if mas_caro else None}")


if __name__ == "__main__":
    main()