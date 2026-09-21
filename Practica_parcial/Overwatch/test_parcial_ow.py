"""
Simulacro de Parcial - Diseño y Algoritmos Orientados a Objetos (Python)
Temática: Overwatch - Temporada de partidas

Ejecución (desde la carpeta donde estén main.py, los CSV y este archivo):
    pytest test_parcial_ow.py -v
"""
import csv
from abc import ABC
from pathlib import Path

import pytest

from main import (
    Jugador,
    Partida,
    PartidaRapida,
    PartidaCompetitiva,
    Temporada,
    cargarJugadores,
    cargarPartidas,
    cargarTemporada,
)

BASE = Path(__file__).parent
RUTA_JUGADORES = str(BASE / "jugadores_ow.csv")
RUTA_PARTIDAS = str(BASE / "partidas_ow.csv")


# ----------------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------------
@pytest.fixture
def nova():
    return Jugador("Nova_Rookie", 10, "Danio")


@pytest.fixture
def tanke():
    return Jugador("Tanke_Pro", 70, "Tanque")


@pytest.fixture
def medic():
    return Jugador("Medic_Vet", 60, "Apoyo")


@pytest.fixture
def temporada_vacia():
    return Temporada("Temporada de prueba")


@pytest.fixture
def temporada_cargada(nova, tanke, medic):
    """
    Experiencia esperada (en orden de inserción) y duración:
      p1 = 187.5   (rápida,      10 min, Nova_Rookie)
      p2 = 375.0   (rápida,      15 min, Medic_Vet)
      p3 = 724.0   (competitiva, 20 min, Tanke_Pro)
      p4 = 305.0   (competitiva, 30 min, Medic_Vet)
    """
    t = Temporada("Temporada de prueba")
    t.addPartida(PartidaRapida(1, "Kings Row", 10, 5, False, nova, False))
    t.addPartida(PartidaRapida(2, "Ilios", 15, 10, True, medic, True))
    t.addPartida(PartidaCompetitiva(3, "Numbani", 20, 10, True, tanke, 2))
    t.addPartida(PartidaCompetitiva(4, "Route 66", 30, 20, False, medic, 0))
    return t


# ======================================================================
# 1. Clase asociada: Jugador
# ======================================================================
class TestJugador:
    def test_atributos(self):
        j = Jugador("Ana_Sniper", 72, "Apoyo")
        assert j.battletag == "Ana_Sniper"
        assert j.nivel == 72
        assert j.rol == "Apoyo"

    def test_asignacion_directa_sin_validaciones(self):
        j = Jugador("X", -5, "Cualquiera")
        assert j.nivel == -5
        assert j.rol == "Cualquiera"


# ======================================================================
# 2. Abstracción
# ======================================================================
class TestAbstraccion:
    def test_partida_es_abc(self):
        assert issubclass(Partida, ABC)

    def test_partida_declara_metodo_abstracto(self):
        assert "calcularExperiencia" in Partida.__abstractmethods__

    def test_partida_no_se_puede_instanciar(self, nova):
        with pytest.raises(TypeError):
            Partida(1, "Kings Row", 10, 5, True, nova)

    def test_subclase_incompleta_no_se_puede_instanciar(self, nova):
        class Incompleta(Partida):
            pass

        with pytest.raises(TypeError):
            Incompleta(1, "Kings Row", 10, 5, True, nova)


# ======================================================================
# 3. Herencia
# ======================================================================
class TestHerencia:
    def test_rapida_hereda_de_partida(self):
        assert issubclass(PartidaRapida, Partida)

    def test_competitiva_hereda_de_partida(self):
        assert issubclass(PartidaCompetitiva, Partida)

    def test_rapida_atributos_propios_y_heredados(self, nova):
        p = PartidaRapida(7, "Dorado", 15, 12, True, nova, True)
        assert isinstance(p, Partida)
        assert p.idPartida == 7
        assert p.mapa == "Dorado"
        assert p.duracionMinutos == 15
        assert p.eliminaciones == 12
        assert p.victoria is True
        assert p.jugador is nova
        assert p.eventoEspecial is True

    def test_competitiva_atributos_propios_y_heredados(self, tanke):
        p = PartidaCompetitiva(8, "Eichenwalde", 35, 25, False, tanke, 4)
        assert isinstance(p, Partida)
        assert p.idPartida == 8
        assert p.mapa == "Eichenwalde"
        assert p.duracionMinutos == 35
        assert p.eliminaciones == 25
        assert p.victoria is False
        assert p.jugador is tanke
        assert p.racha == 4

    def test_agregacion_el_jugador_es_el_mismo_objeto(self, medic):
        p = PartidaRapida(1, "Ilios", 10, 5, True, medic, False)
        medic.nivel = 99
        assert p.jugador.nivel == 99  # referencia, no copia


# ======================================================================
# 4. Polimorfismo: calcularExperiencia()
# ======================================================================
class TestExperienciaRapida:
    @pytest.mark.parametrize(
        "duracion, elim, victoria, evento, nivel, esperado",
        [
            # Derrota, sin evento, nivel 10 (<50 -> x1.5): (100 + 25) * 1.5
            (10, 5, False, False, 10, 187.5),
            # Borde: nivel 50 ya NO recibe el bono de novato
            (10, 5, False, False, 50, 125.0),
            # Borde: nivel 49 SÍ lo recibe
            (10, 5, False, False, 49, 187.5),
            # Victoria + evento, nivel 60: (150 + 50 + 100) * 1.25
            (15, 10, True, True, 60, 375.0),
            # Victoria sin evento, nivel 72: 120 + 50 + 100
            (12, 10, True, False, 72, 270.0),
            # Derrota, nivel 8: (80 + 15) * 1.5
            (8, 3, False, False, 8, 142.5),
            # Todo junto: victoria + evento + novato: (180 + 70 + 100) * 1.25 * 1.5
            (18, 14, True, True, 41, 656.25),
            # Partida vacía
            (0, 0, False, False, 99, 0.0),
        ],
    )
    def test_calculo(self, duracion, elim, victoria, evento, nivel, esperado):
        j = Jugador("Test", nivel, "Danio")
        p = PartidaRapida(1, "Mapa", duracion, elim, victoria, j, evento)
        assert p.calcularExperiencia() == pytest.approx(esperado)

    def test_el_rol_no_influye_en_rapida(self):
        a = PartidaRapida(1, "M", 10, 5, True, Jugador("A", 70, "Tanque"), False)
        b = PartidaRapida(2, "M", 10, 5, True, Jugador("B", 70, "Danio"), False)
        assert a.calcularExperiencia() == pytest.approx(b.calcularExperiencia())


class TestExperienciaCompetitiva:
    @pytest.mark.parametrize(
        "duracion, elim, victoria, racha, rol, esperado",
        [
            # Victoria, racha 2, Tanque: (300 + 80) * 1.5 * 1.2 + 40
            (20, 10, True, 2, "Tanque", 724.0),
            # Derrota, racha 0, Apoyo: (450 + 160) * 0.5
            (30, 20, False, 0, "Apoyo", 305.0),
            # Racha con tope en 5: (525 + 200) * 1.5 * 1.5 + 40
            (35, 25, True, 8, "Tanque", 1671.25),
            # Racha exactamente en el tope: mismo resultado que racha 8
            (35, 25, True, 5, "Tanque", 1671.25),
            # Derrota con racha 3, Danio: (420 + 80) * 0.5 * 1.3
            (28, 10, False, 3, "Danio", 325.0),
            # El bono de Tanque se suma AL FINAL, sin multiplicarse
            (22, 12, True, 2, "Apoyo", 766.8),
            # Danio no recibe bono: (300 + 80) * 1.5
            (20, 10, True, 0, "Danio", 570.0),
            # Tanque en derrota sin racha: 150 * 0.5 + 40
            (10, 0, False, 0, "Tanque", 115.0),
        ],
    )
    def test_calculo(self, duracion, elim, victoria, racha, rol, esperado):
        j = Jugador("Test", 70, rol)
        p = PartidaCompetitiva(1, "Mapa", duracion, elim, victoria, j, racha)
        assert p.calcularExperiencia() == pytest.approx(esperado)

    def test_el_nivel_no_influye_en_competitiva(self):
        a = PartidaCompetitiva(1, "M", 10, 5, True, Jugador("A", 5, "Danio"), 0)
        b = PartidaCompetitiva(2, "M", 10, 5, True, Jugador("B", 99, "Danio"), 0)
        assert a.calcularExperiencia() == pytest.approx(b.calcularExperiencia())


class TestPolimorfismo:
    def test_lista_heterogenea(self, temporada_cargada):
        xp = [p.calcularExperiencia() for p in temporada_cargada.partidas]
        assert xp == pytest.approx([187.5, 375.0, 724.0, 305.0])


# ======================================================================
# 5. Contenedor: Temporada
# ======================================================================
class TestTemporadaBasico:
    def test_init_lista_vacia(self, temporada_vacia):
        assert temporada_vacia.nombre == "Temporada de prueba"
        assert temporada_vacia.partidas == []

    def test_listas_no_compartidas_entre_instancias(self, nova):
        t1 = Temporada("A")
        t2 = Temporada("B")
        t1.addPartida(PartidaRapida(1, "Ilios", 10, 5, True, nova, False))
        assert len(t1.partidas) == 1
        assert len(t2.partidas) == 0

    def test_add_partida_mantiene_orden(self, temporada_vacia, nova):
        a = PartidaRapida(1, "Ilios", 10, 5, True, nova, False)
        b = PartidaCompetitiva(2, "Numbani", 20, 10, True, nova, 1)
        temporada_vacia.addPartida(a)
        temporada_vacia.addPartida(b)
        assert len(temporada_vacia.partidas) == 2
        assert temporada_vacia.partidas[0] is a
        assert temporada_vacia.partidas[1] is b


class TestTotales:
    def test_experiencia_total(self, temporada_cargada):
        assert temporada_cargada.experienciaTotal() == pytest.approx(1591.5)

    def test_experiencia_total_vacia(self, temporada_vacia):
        assert temporada_vacia.experienciaTotal() == 0.0

    def test_experiencia_por_jugador(self, temporada_cargada):
        # Medic_Vet: 375 + 305
        assert temporada_cargada.experienciaPorJugador("Medic_Vet") == pytest.approx(680.0)
        assert temporada_cargada.experienciaPorJugador("Nova_Rookie") == pytest.approx(187.5)

    def test_experiencia_por_jugador_inexistente(self, temporada_cargada):
        assert temporada_cargada.experienciaPorJugador("Fantasma") == 0.0

    def test_experiencia_por_jugador_vacia(self, temporada_vacia):
        assert temporada_vacia.experienciaPorJugador("Medic_Vet") == 0.0


class TestPromedioEnRango:
    def test_rango_intermedio(self, temporada_cargada):
        # Entran 375, 724 y 305 -> 1404 / 3
        assert temporada_cargada.promedioEnRango(300.0, 800.0) == pytest.approx(468.0)

    def test_limites_inclusivos(self, temporada_cargada):
        # 187.5 y 305.0 son valores exactos y quedan justo en los extremos
        assert temporada_cargada.promedioEnRango(187.5, 305.0) == pytest.approx(246.25)

    def test_un_solo_elemento(self, temporada_cargada):
        assert temporada_cargada.promedioEnRango(375.0, 375.0) == pytest.approx(375.0)

    def test_sin_coincidencias(self, temporada_cargada):
        assert temporada_cargada.promedioEnRango(5000.0, 9000.0) == 0.0

    def test_temporada_vacia(self, temporada_vacia):
        assert temporada_vacia.promedioEnRango(0.0, 9999.0) == 0.0


class TestBusquedas:
    def test_primera_de_jugador_devuelve_la_primera(self, temporada_cargada):
        # Medic_Vet tiene las partidas 2 y 4: debe devolver la 2
        r = temporada_cargada.buscarPrimeraDeJugador("Medic_Vet")
        assert r is temporada_cargada.partidas[1]
        assert r.idPartida == 2

    def test_primera_de_jugador_inexistente(self, temporada_cargada):
        assert temporada_cargada.buscarPrimeraDeJugador("Fantasma") is None

    def test_primera_de_jugador_vacia(self, temporada_vacia):
        assert temporada_vacia.buscarPrimeraDeJugador("Medic_Vet") is None

    def test_primera_mayor_a_no_es_la_maxima(self, temporada_cargada):
        # La primera que supera 300 es la 2 (375), aunque la 3 (724) sea mayor
        r = temporada_cargada.buscarPrimeraMayorA(300.0)
        assert r is not None
        assert r.idPartida == 2

    def test_primera_mayor_a_es_estricto(self, temporada_cargada):
        # La 2 vale exactamente 375: no es "mayor a 375"; la primera que lo es es la 3
        assert temporada_cargada.buscarPrimeraMayorA(375.0).idPartida == 3

    def test_primera_mayor_a_sin_coincidencias(self, temporada_cargada):
        assert temporada_cargada.buscarPrimeraMayorA(5000.0) is None

    def test_primera_mayor_a_vacia(self, temporada_vacia):
        assert temporada_vacia.buscarPrimeraMayorA(0.0) is None

    def test_corte_temprano(self, temporada_vacia, tanke):
        """
        Después de la partida que cumple agrego una "bomba" que falla si se le
        calcula la experiencia. Una búsqueda que recorra de más explota.
        """

        class Bomba(Partida):
            def calcularExperiencia(self):
                raise AssertionError("La búsqueda debió cortar antes de llegar acá")

        cumple = PartidaCompetitiva(1, "Numbani", 20, 10, True, tanke, 2)
        temporada_vacia.addPartida(cumple)
        temporada_vacia.addPartida(Bomba(2, "Bomba", 1, 0, False, tanke))
        assert temporada_vacia.buscarPrimeraMayorA(500.0) is cumple


class TestConteoYMaximo:
    def test_contar_por_tipo(self, temporada_cargada):
        assert temporada_cargada.contarPorTipo(PartidaRapida) == 2
        assert temporada_cargada.contarPorTipo(PartidaCompetitiva) == 2

    def test_contar_por_clase_base(self, temporada_cargada):
        assert temporada_cargada.contarPorTipo(Partida) == 4

    def test_contar_por_tipo_vacia(self, temporada_vacia):
        assert temporada_vacia.contarPorTipo(PartidaRapida) == 0

    def test_partida_mas_larga(self, temporada_cargada):
        # Se compara por DURACIÓN (no por experiencia): gana la 4 con 30 minutos
        r = temporada_cargada.partidaMasLarga()
        assert r.idPartida == 4
        assert r.duracionMinutos == 30

    def test_partida_mas_larga_vacia(self, temporada_vacia):
        assert temporada_vacia.partidaMasLarga() is None


# ======================================================================
# 6. Carga desde CSV (main.py)
#    partidas_ow.csv es UN solo archivo: la columna "tipo" indica la clase
#    (tipo 1 -> PartidaRapida / tipo 2 -> PartidaCompetitiva)
# ======================================================================
class TestCargaCSV:
    def test_cargar_jugadores(self):
        jugadores = cargarJugadores(RUTA_JUGADORES)
        assert isinstance(jugadores, dict)
        assert len(jugadores) == 12
        a = jugadores["Ana_Sniper"]
        assert isinstance(a, Jugador)
        assert a.nivel == 72 and isinstance(a.nivel, int)
        assert a.rol == "Apoyo"
        assert jugadores["Junkrat_Boom"].nivel == 8
        assert jugadores["Junkrat_Boom"].rol == "Danio"

    def test_cargar_partidas_cantidad_y_tipos(self):
        jugadores = cargarJugadores(RUTA_JUGADORES)
        partidas = cargarPartidas(RUTA_PARTIDAS, jugadores)
        assert len(partidas) == 16
        clases = {"1": PartidaRapida, "2": PartidaCompetitiva}
        with open(RUTA_PARTIDAS, encoding="utf-8", newline="") as f:
            filas = list(csv.DictReader(f))
        for fila, p in zip(filas, partidas):
            assert type(p) is clases[fila["tipo"]]
            assert p.idPartida == int(fila["idPartida"])
        assert sum(isinstance(p, PartidaRapida) for p in partidas) == 8
        assert sum(isinstance(p, PartidaCompetitiva) for p in partidas) == 8

    def test_rapida_desde_csv(self):
        jugadores = cargarJugadores(RUTA_JUGADORES)
        partidas = cargarPartidas(RUTA_PARTIDAS, jugadores)
        p = partidas[0]
        assert isinstance(p, PartidaRapida)
        assert p.idPartida == 1 and isinstance(p.idPartida, int)
        assert p.mapa == "Kings Row"
        assert p.duracionMinutos == 12 and isinstance(p.duracionMinutos, int)
        assert p.eliminaciones == 10 and isinstance(p.eliminaciones, int)
        assert p.victoria is True
        assert p.eventoEspecial is False
        assert p.jugador is jugadores["Ana_Sniper"]
        # id 3: derrota con evento especial
        assert partidas[2].victoria is False
        assert partidas[2].eventoEspecial is True

    def test_competitiva_desde_csv(self):
        jugadores = cargarJugadores(RUTA_JUGADORES)
        partidas = cargarPartidas(RUTA_PARTIDAS, jugadores)
        p = partidas[1]
        assert isinstance(p, PartidaCompetitiva)
        assert p.idPartida == 2
        assert p.mapa == "Numbani"
        assert p.duracionMinutos == 25
        assert p.eliminaciones == 18
        assert p.victoria is True
        assert p.racha == 3 and isinstance(p.racha, int)
        assert p.jugador is jugadores["Genji_Main"]
        assert partidas[7].racha == 8  # id 8

    def test_experiencia_de_filas_conocidas(self):
        jugadores = cargarJugadores(RUTA_JUGADORES)
        partidas = cargarPartidas(RUTA_PARTIDAS, jugadores)
        assert partidas[0].calcularExperiencia() == pytest.approx(270.0)     # id 1
        assert partidas[1].calcularExperiencia() == pytest.approx(1012.05)   # id 2
        assert partidas[5].calcularExperiencia() == pytest.approx(142.5)     # id 6
        assert partidas[7].calcularExperiencia() == pytest.approx(1671.25)   # id 8


class TestTemporadaDesdeCSV:
    @pytest.fixture
    def temporada(self):
        return cargarTemporada(RUTA_JUGADORES, RUTA_PARTIDAS)

    def test_estructura(self, temporada):
        assert isinstance(temporada, Temporada)
        assert temporada.nombre == "Temporada Actual"
        assert len(temporada.partidas) == 16
        # Las partidas quedan en el mismo orden del archivo
        assert [p.idPartida for p in temporada.partidas] == list(range(1, 17))

    def test_conteos(self, temporada):
        assert temporada.contarPorTipo(PartidaRapida) == 8
        assert temporada.contarPorTipo(PartidaCompetitiva) == 8

    def test_experiencia_total(self, temporada):
        assert temporada.experienciaTotal() == pytest.approx(9485.225)

    def test_experiencia_por_jugador(self, temporada):
        assert temporada.experienciaPorJugador("Ana_Sniper") == pytest.approx(410.0)
        assert temporada.experienciaPorJugador("RoadHog_Pro") == pytest.approx(1548.0)
        assert temporada.experienciaPorJugador("NoExiste") == 0.0

    def test_promedio_en_rango(self, temporada):
        assert temporada.promedioEnRango(300.0, 800.0) == pytest.approx(612.15)
        assert temporada.promedioEnRango(0.0, 150.0) == pytest.approx(141.25)
        assert temporada.promedioEnRango(5000.0, 9000.0) == 0.0

    def test_busquedas(self, temporada):
        # Ana_Sniper juega las partidas 1 y 13: gana la primera
        assert temporada.buscarPrimeraDeJugador("Ana_Sniper").idPartida == 1
        assert temporada.buscarPrimeraDeJugador("RoadHog_Pro").idPartida == 4
        assert temporada.buscarPrimeraMayorA(700.0).idPartida == 2
        assert temporada.buscarPrimeraMayorA(1100.0).idPartida == 8
        assert temporada.buscarPrimeraMayorA(2000.0) is None

    def test_partida_mas_larga(self, temporada):
        r = temporada.partidaMasLarga()
        assert r.idPartida == 8
        assert r.mapa == "Eichenwalde"
        assert r.duracionMinutos == 35
