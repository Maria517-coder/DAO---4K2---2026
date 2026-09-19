import pytest

from jugador import Jugador
from crafteo import Crafteo
from crafteoArma import CrafteoArma
from crafteoPocion import CrafteoPocion
from tallerCrafteo import Taller


@pytest.fixture()
def taller():
    t = Taller()
    t.addCrafteo(CrafteoArma(1, "Espada de hierro", 20.0, 2, Jugador("NOVA", 5, "Novato"), 6, False))
    t.addCrafteo(CrafteoArma(2, "Hacha de netherita", 90.0, 1, Jugador("LEGO", 80, "Leyenda"), 10, True))
    t.addCrafteo(CrafteoPocion(3, "Pocion de curacion", 12.0, 3, Jugador("VERA", 40, "Veterano"), 2, False))
    t.addCrafteo(CrafteoPocion(4, "Pocion de fuerza", 20.0, 1, Jugador("NOVA", 5, "Novato"), 1, True))
    return t


# ---------------------------------------------------------------- Jugador
def test_jugador_atributos():
    j = Jugador("STEVE", 45, "Veterano")
    assert j.nickname == "STEVE"
    assert j.nivel == 45
    assert j.rango == "Veterano"


# ---------------------------------------------------------------- Abstracción
def test_crafteo_no_se_puede_instanciar():
    with pytest.raises(TypeError):
        Crafteo(1, "Algo", 10.0, 1, Jugador("NOVA", 5, "Novato"))


def test_subclase_sin_calcularCostoFinal_no_se_puede_instanciar():
    class Incompleta(Crafteo):
        pass

    with pytest.raises(TypeError):
        Incompleta(1, "Algo", 10.0, 1, Jugador("NOVA", 5, "Novato"))


# ---------------------------------------------------------------- Herencia
def test_arma_hereda_de_crafteo():
    assert issubclass(CrafteoArma, Crafteo)


def test_pocion_hereda_de_crafteo():
    assert issubclass(CrafteoPocion, Crafteo)


def test_arma_atributos():
    j = Jugador("NOVA", 5, "Novato")
    arma = CrafteoArma(7, "Ballesta", 40.0, 2, j, 6, True)
    assert arma.idCrafteo == 7
    assert arma.item == "Ballesta"
    assert arma.costoBase == 40.0
    assert arma.cantidad == 2
    assert arma.jugador is j
    assert arma.danio == 6
    assert arma.encantada is True


def test_pocion_atributos():
    j = Jugador("VERA", 40, "Veterano")
    pocion = CrafteoPocion(8, "Pocion de salto", 8.0, 6, j, 1, True)
    assert pocion.idCrafteo == 8
    assert pocion.item == "Pocion de salto"
    assert pocion.costoBase == 8.0
    assert pocion.cantidad == 6
    assert pocion.jugador is j
    assert pocion.potencia == 1
    assert pocion.splash is True


# ---------------------------------------------------------------- Costo arma
def test_costo_arma_novato_sin_encantar():
    arma = CrafteoArma(1, "Espada", 20.0, 2, Jugador("NOVA", 5, "Novato"), 6, False)
    # (20 + 6 * 1.5) * 2
    assert arma.calcularCostoFinal() == pytest.approx(58.0)


def test_costo_arma_novato_encantada():
    arma = CrafteoArma(2, "Espada", 50.0, 1, Jugador("NOVA", 5, "Novato"), 7, True)
    # (50 + 7 * 1.5) * 1 * 1.25
    assert arma.calcularCostoFinal() == pytest.approx(75.625)


def test_costo_arma_veterano_descuento_10():
    arma = CrafteoArma(3, "Hacha", 60.0, 2, Jugador("VERA", 40, "Veterano"), 9, False)
    # (60 + 9 * 1.5) * 2 * 0.90
    assert arma.calcularCostoFinal() == pytest.approx(132.3)


def test_costo_arma_leyenda_encantada_descuento_20():
    arma = CrafteoArma(4, "Hacha", 90.0, 1, Jugador("LEGO", 80, "Leyenda"), 10, True)
    # (90 + 10 * 1.5) * 1.25 * 0.80
    assert arma.calcularCostoFinal() == pytest.approx(105.0)


def test_costo_arma_aventurero_sin_descuento():
    arma = CrafteoArma(5, "Espada", 25.0, 1, Jugador("ENDER", 22, "Aventurero"), 4, False)
    # 25 + 4 * 1.5
    assert arma.calcularCostoFinal() == pytest.approx(31.0)


def test_costo_arma_sin_danio():
    arma = CrafteoArma(6, "Palo", 10.0, 1, Jugador("NOVA", 5, "Novato"), 0, False)
    assert arma.calcularCostoFinal() == pytest.approx(10.0)


def test_costo_arma_el_descuento_depende_del_rango_no_del_nivel():
    arma = CrafteoArma(6, "Palo", 10.0, 1, Jugador("NOVA", 99, "Novato"), 0, False)
    assert arma.calcularCostoFinal() == pytest.approx(10.0)


# ---------------------------------------------------------------- Costo poción
def test_costo_pocion_nivel_29_sin_descuento():
    pocion = CrafteoPocion(1, "Curacion", 12.0, 3, Jugador("DAVE", 29, "Aventurero"), 2, False)
    # 12 * 2 * 3
    assert pocion.calcularCostoFinal() == pytest.approx(72.0)


def test_costo_pocion_nivel_30_con_descuento():
    pocion = CrafteoPocion(2, "Curacion", 12.0, 3, Jugador("PIXEL", 30, "Veterano"), 2, False)
    # 12 * 2 * 3 * 0.90
    assert pocion.calcularCostoFinal() == pytest.approx(64.8)


def test_costo_pocion_splash_sin_descuento():
    pocion = CrafteoPocion(3, "Fuerza", 20.0, 1, Jugador("NOVA", 5, "Novato"), 1, True)
    # 20 * 1 * 1 + 15 * 1
    assert pocion.calcularCostoFinal() == pytest.approx(35.0)


def test_costo_pocion_splash_con_descuento():
    pocion = CrafteoPocion(4, "Regeneracion", 18.0, 2, Jugador("CREEPER", 78, "Leyenda"), 3, True)
    # (18 * 3 * 2 + 15 * 2) * 0.90
    assert pocion.calcularCostoFinal() == pytest.approx(124.2)


def test_costo_pocion_el_descuento_no_se_acumula():
    pocion = CrafteoPocion(5, "Invisibilidad", 25.0, 1, Jugador("HERO", 100, "Leyenda"), 1, False)
    # 25 * 0.90
    assert pocion.calcularCostoFinal() == pytest.approx(22.5)


def test_costo_pocion_el_rango_no_influye():
    a = CrafteoPocion(6, "P", 10.0, 1, Jugador("A", 10, "Leyenda"), 1, False)
    b = CrafteoPocion(7, "P", 10.0, 1, Jugador("B", 10, "Novato"), 1, False)
    assert a.calcularCostoFinal() == pytest.approx(b.calcularCostoFinal())


# ---------------------------------------------------------------- Taller
def test_taller_comienza_vacio():
    t = Taller()
    assert t.crafteos == []
    assert t.totalRecaudado() == 0
    assert t.totalPorJugador("NOVA") == 0
    assert t.promedioEnRango(0, 9999) == 0
    assert t.buscarPrimeroDeJugador("NOVA") is None
    assert t.buscarPrimeroMayorA(0) is None
    assert t.contarPorTipo(CrafteoArma) == 0
    assert t.crafteoMasCaro() is None


def test_talleres_no_comparten_lista():
    t1 = Taller()
    t2 = Taller()
    t1.addCrafteo(CrafteoArma(1, "Arco", 15.0, 1, Jugador("NOVA", 5, "Novato"), 5, False))
    assert len(t1.crafteos) == 1
    assert len(t2.crafteos) == 0


def test_addCrafteo_crafteos(taller):
    assert len(taller.crafteos) == 4
    assert taller.crafteos[0].idCrafteo == 1
    assert taller.crafteos[3].idCrafteo == 4


def test_costos_polimorficos(taller):
    costos = [c.calcularCostoFinal() for c in taller.crafteos]
    assert costos == pytest.approx([58.0, 105.0, 64.8, 35.0])


def test_totalRecaudado(taller):
    # 58 + 105 + 64.8 + 35
    assert taller.totalRecaudado() == pytest.approx(262.8)


def test_totalPorJugador(taller):
    # NOVA: 58 + 35
    assert taller.totalPorJugador("NOVA") == pytest.approx(93.0)
    assert taller.totalPorJugador("LEGO") == pytest.approx(105.0)


def test_totalPorJugador_inexistente(taller):
    assert taller.totalPorJugador("FANTASMA") == 0


def test_promedioEnRango(taller):
    # entran 58, 105 y 64.8
    assert taller.promedioEnRango(50, 110) == pytest.approx(227.8 / 3)


def test_promedioEnRango_limites_inclusivos(taller):
    # 35 y 58 quedan justo en los extremos: (35 + 58) / 2
    assert taller.promedioEnRango(35, 58) == pytest.approx(46.5)


def test_promedioEnRango_sin_coincidencias(taller):
    assert taller.promedioEnRango(1000, 2000) == 0


def test_buscarPrimeroDeJugador(taller):
    # NOVA tiene los crafteos 1 y 4: debe devolver el 1
    assert taller.buscarPrimeroDeJugador("NOVA").idCrafteo == 1


def test_buscarPrimeroDeJugador_inexistente(taller):
    assert taller.buscarPrimeroDeJugador("FANTASMA") is None


def test_buscarPrimeroMayorA(taller):
    assert taller.buscarPrimeroMayorA(100).idCrafteo == 2


def test_buscarPrimeroMayorA_es_estricto(taller):
    # el crafteo 1 cuesta exactamente 58: no es mayor a 58
    assert taller.buscarPrimeroMayorA(58).idCrafteo == 2


def test_buscarPrimeroMayorA_sin_coincidencias(taller):
    assert taller.buscarPrimeroMayorA(500) is None


def test_buscarPrimeroMayorA_corta_en_el_primero():
    class Bomba(Crafteo):
        def calcularCostoFinal(self):
            raise AssertionError("la busqueda debio cortar antes")

    t = Taller()
    cumple = CrafteoArma(1, "Hacha", 90.0, 1, Jugador("LEGO", 80, "Leyenda"), 10, True)
    t.addCrafteo(cumple)
    t.addCrafteo(Bomba(2, "Bomba", 1.0, 1, Jugador("LEGO", 80, "Leyenda")))
    assert t.buscarPrimeroMayorA(100) is cumple


def test_contarPorTipo(taller):
    assert taller.contarPorTipo(CrafteoArma) == 2
    assert taller.contarPorTipo(CrafteoPocion) == 2


def test_contar_por_clase_base(taller):
    assert taller.contarPorTipo(Crafteo) == 4


def test_crafteoMasCaro(taller):
    mas_caro = taller.crafteoMasCaro()
    assert mas_caro.idCrafteo == 2
    assert mas_caro.calcularCostoFinal() == pytest.approx(105.0)
