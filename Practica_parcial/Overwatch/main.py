from partida import Partida
from partidaRapida import PartidaRapida
from partidaCompetitiva import PartidaCompetitiva
from jugador import Jugador
from temporada import Temporada


def main():
    # csv jugadores
    jugadores = {}
    texto2 = open("jugadores_ow.csv")
    texto2.readline()
    for linea in texto2:
        datos = linea.strip().split(",")
        battletag = datos[0]
        nivel = int(datos[1])
        rol = datos[2]
        jugadores[battletag] = Jugador(battletag, nivel, rol)

    texto2.close()

    # csv partidas
    instancia = Temporada("Rosa Pastel")
    texto = open("partidas_ow.csv")
    texto.readline()
    for linea in texto:
        datos = linea.strip().split(",")
        tipo = int(datos[0])
        idPartida = int(datos[1])
        mapa = datos[2]
        duracionMinutos = int(datos[3])
        eliminaciones = int(datos[4])
        victoria = datos[5] == "si"
        battletag = datos[6]

        # Relaciono los dos csv por el battletag de ESTA fila
        jugador_obj = jugadores[battletag]

        if tipo == 1:
            eventoEspecial = datos[7] == "si"
            partida = PartidaRapida(idPartida, mapa, duracionMinutos, eliminaciones, victoria, jugador_obj, eventoEspecial)

        elif tipo == 2:
            racha = int(datos[7])
            partida = PartidaCompetitiva(idPartida, mapa, duracionMinutos, eliminaciones, victoria, jugador_obj, racha)

        instancia.addPartida(partida)

    texto.close()

    print(instancia.experienciaTotal())
    print(instancia.experienciaPorJugador("Genji_Main"))
    print(instancia.promedioEnRango(0, 100))
    print(instancia.buscarPrimeraDeJugador("Genji_Main"))
    print(instancia.buscarPrimeraMayorA(3))
    print(instancia.contarPorTipo(PartidaCompetitiva))
    print(instancia.partidaMasLarga())


if __name__ == "__main__":
    main()