"""Pruebas del ejercicio "El pool de campeones".

Las clases se buscan por nombre (Campeon, Mago, Tanque y Equipo) en los módulos
.py que estén en la misma carpeta que este archivo, de modo que la solución
puede estar en uno o en varios módulos, con los nombres de archivo que prefieras.

    python -m pytest -v
"""

import importlib
import sys
from pathlib import Path

import pytest

CARPETA = Path(__file__).resolve().parent
NOMBRES_REQUERIDOS = ("Campeon", "Mago", "Tanque", "Equipo")


def _buscar_clases():
    """Devuelve ({nombre: clase}, {archivo: error}) recorriendo los .py de la carpeta."""
    if str(CARPETA) not in sys.path:
        sys.path.insert(0, str(CARPETA))
    encontradas, errores = {}, {}
    for archivo in sorted(CARPETA.glob("*.py")):
        if archivo.stem.startswith(("test_", "__")) or archivo.stem == "conftest":
            continue
        try:
            modulo = importlib.import_module(archivo.stem)
        except (Exception, SystemExit) as error:
            errores[archivo.name] = f"{type(error).__name__}: {error}"
            continue
        for nombre in NOMBRES_REQUERIDOS:
            candidata = getattr(modulo, nombre, None)
            if isinstance(candidata, type):
                encontradas.setdefault(nombre, candidata)
    return encontradas, errores


CLASES, ERRORES_DE_IMPORTACION = _buscar_clases()


def _clase(nombre):
    if nombre not in CLASES:
        detalle = f" Errores al importar: {ERRORES_DE_IMPORTACION}." if ERRORES_DE_IMPORTACION else ""
        pytest.fail(f"No se encontró la clase {nombre} en los módulos de {CARPETA}.{detalle}", pytrace=False)
    return CLASES[nombre]


# Constructores auxiliares: los valores por defecto no influyen en los resultados
# (cada prueba indica explícitamente los que sí importan).

def _mago(codigo=1, nombre="Annie", partidas=100, poder_base=500.0,
          habilidades_area=0, prioridad_baneo=False):
    return _clase("Mago")(codigo, nombre, partidas, poder_base, habilidades_area, prioridad_baneo)


def _tanque(codigo=2, nombre="Malphite", partidas=100, poder_base=500.0,
            armadura=0.0, dificultad=10):
    return _clase("Tanque")(codigo, nombre, partidas, poder_base, armadura, dificultad)


def _equipo(*campeones):
    equipo = _clase("Equipo")()
    for campeon in campeones:
        equipo.agregar(campeon)
    return equipo


class TestCampeon:
    def test_guarda_sus_atributos(self):
        campeon = _clase("Campeon")(30, "Karthus", 320, 540.0)
        assert campeon.codigo == 30
        assert campeon.nombre == "Karthus"
        assert campeon.partidas == 320
        assert campeon.poder_base == 540.0

    def test_su_poder_es_el_poder_base(self):
        campeon = _clase("Campeon")(30, "Karthus", 320, 540.0)
        assert campeon.poder() == pytest.approx(540.0)


class TestMago:
    def test_es_un_campeon_y_conserva_los_atributos_heredados(self):
        mago = _mago(codigo=30, nombre="Karthus", partidas=320, poder_base=540.0)
        assert isinstance(mago, _clase("Campeon"))
        assert (mago.codigo, mago.nombre, mago.partidas, mago.poder_base) == (30, "Karthus", 320, 540.0)

    @pytest.mark.parametrize("habilidades_area, prioridad_baneo, adicional", [
        (0, False, 0.0),     # sin adicionales
        (3, False, 90.0),    # 30 por cada habilidad de daño en área
        (0, True, 100.0),    # 100 por prioridad de baneo
        (4, True, 220.0),    # ambos adicionales
    ])
    def test_poder_definitivo(self, habilidades_area, prioridad_baneo, adicional):
        mago = _mago(poder_base=500.0, habilidades_area=habilidades_area, prioridad_baneo=prioridad_baneo)
        assert mago.poder() == pytest.approx(500.0 + adicional)


class TestTanque:
    def test_es_un_campeon_y_conserva_los_atributos_heredados(self):
        tanque = _tanque(codigo=54, nombre="Malphite", partidas=310, poder_base=430.0)
        assert isinstance(tanque, _clase("Campeon"))
        assert (tanque.codigo, tanque.nombre, tanque.partidas, tanque.poder_base) == (54, "Malphite", 310, 430.0)

    @pytest.mark.parametrize("dificultad, bonificacion", [
        (1, 20.0),
        (3, 20.0),    # menor a 4: todavía recibe la bonificación
        (4, 0.0),     # 4 ya no la recibe
        (10, 0.0),
    ])
    def test_poder_definitivo(self, dificultad, bonificacion):
        # La armadura siempre se incorpora; la bonificación depende de la dificultad.
        tanque = _tanque(poder_base=400.0, armadura=40.5, dificultad=dificultad)
        assert tanque.poder() == pytest.approx(440.5 + bonificacion)


class TestEquipo:
    def test_equipo_vacio(self):
        equipo = _equipo()
        assert equipo.suma_poderes() == 0
        assert equipo.cantidad_magos_elite() == 0
        assert equipo.nombre_tanque_mas_debil() is None

    def test_cada_equipo_tiene_su_propia_coleccion(self):
        uno = _equipo(_mago(poder_base=500.0))
        otro = _equipo()
        assert uno.suma_poderes() == pytest.approx(500.0)
        assert otro.suma_poderes() == 0

    def test_suma_poderes_de_campeones_de_ambos_tipos(self):
        equipo = _equipo(
            _mago(poder_base=540.0, habilidades_area=3, prioridad_baneo=True),   # 730.0
            _mago(poder_base=455.5, habilidades_area=1),                         # 485.5
            _tanque(poder_base=430.0, armadura=47.0, dificultad=2),              # 497.0
            _tanque(poder_base=455.5, armadura=50.5, dificultad=4),              # 506.0
        )
        assert equipo.suma_poderes() == pytest.approx(2218.5)

    def test_cuenta_solo_los_magos_que_cumplen_las_tres_condiciones(self):
        equipo = _equipo(
            _mago(partidas=320, habilidades_area=3, prioridad_baneo=True),    # élite
            _mago(partidas=190, habilidades_area=4, prioridad_baneo=True),    # élite
            _mago(partidas=60, habilidades_area=4, prioridad_baneo=True),     # pocas partidas
            _mago(partidas=400, habilidades_area=1, prioridad_baneo=True),    # pocas habilidades
            _mago(partidas=400, habilidades_area=4, prioridad_baneo=False),   # sin prioridad de baneo
        )
        assert equipo.cantidad_magos_elite() == 2

    @pytest.mark.parametrize("partidas, habilidades_area, prioridad_baneo, esperado", [
        (151, 3, True, 1),
        (150, 3, True, 0),    # "más de 150": 150 no alcanza
        (200, 2, True, 0),    # "más de 2": 2 no alcanza
        (200, 4, False, 0),   # falta la prioridad de baneo
    ])
    def test_los_limites_de_magos_elite_son_estrictos(self, partidas, habilidades_area, prioridad_baneo, esperado):
        equipo = _equipo(_mago(partidas=partidas, habilidades_area=habilidades_area,
                               prioridad_baneo=prioridad_baneo))
        assert equipo.cantidad_magos_elite() == esperado

    def test_los_tanques_no_cuentan_como_magos_elite(self):
        equipo = _equipo(
            _tanque(partidas=500, armadura=60.0, dificultad=1),
            _mago(partidas=200, habilidades_area=3, prioridad_baneo=True),
        )
        assert equipo.cantidad_magos_elite() == 1

    def test_tanque_mas_debil_devuelve_el_nombre_del_de_menor_poder(self):
        equipo = _equipo(
            _tanque(nombre="Ornn", poder_base=470.0, armadura=44.0, dificultad=5),     # 514.0
            _tanque(nombre="Sion", poder_base=445.0, armadura=41.5, dificultad=5),     # 486.5
            _tanque(nombre="Leona", poder_base=455.5, armadura=50.5, dificultad=4),    # 506.0
        )
        assert equipo.nombre_tanque_mas_debil() == "Sion"

    def test_tanque_mas_debil_compara_el_poder_definitivo_y_no_el_base(self):
        equipo = _equipo(
            _tanque(nombre="Amumu", poder_base=410.0, armadura=38.0, dificultad=3),    # base menor, definitivo 468.0
            _tanque(nombre="Rammus", poder_base=415.0, armadura=52.0, dificultad=6),   # definitivo 467.0
        )
        assert equipo.nombre_tanque_mas_debil() == "Rammus"

    def test_tanque_mas_debil_ignora_a_los_magos(self):
        equipo = _equipo(
            _tanque(nombre="Ornn", poder_base=470.0, armadura=44.0, dificultad=5),        # 514.0
            _mago(nombre="Fiddlesticks", poder_base=380.0, habilidades_area=1),          # 410.0 (menor que cualquier tanque)
            _tanque(nombre="Malphite", poder_base=430.0, armadura=47.0, dificultad=2),    # 497.0
        )
        assert equipo.nombre_tanque_mas_debil() == "Malphite"

    def test_tanque_mas_debil_sin_tanques_devuelve_none(self):
        equipo = _equipo(_mago(habilidades_area=2))
        assert equipo.nombre_tanque_mas_debil() is None