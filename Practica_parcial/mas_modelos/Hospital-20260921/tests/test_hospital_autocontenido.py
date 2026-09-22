"""Suite basica autocontenida del ejercicio Hospital.
Uso:
    pytest tests/test_hospital_autocontenido.py -v
    python  tests/test_hospital_autocontenido.py
"""

import sys
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Bootstrap: agrega la raiz del proyecto (la carpeta Hospital) al sys.path para
# que los modulos se importen igual que lo hace main.py.
# ---------------------------------------------------------------------------


def _raizProyecto() -> Path:
    """Busca hacia arriba la carpeta que contiene los modulos del ejercicio."""
    for carpeta in [Path(__file__).resolve().parent, *Path(__file__).resolve().parents]:
        if (carpeta / "hospital.py").is_file() and (carpeta / "atencion.py").is_file():
            return carpeta
    raise RuntimeError(
        "No se encontro la raiz del proyecto (hospital.py / atencion.py) "
        f"partiendo de {Path(__file__).resolve()}"
    )


RAIZ_PROYECTO = _raizProyecto()
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))

import main  # noqa: E402
from atencion import Atencion, AtencionFarmacia, AtencionMedica  # noqa: E402
from hospital import Hospital  # noqa: E402
from paciente import Paciente  # noqa: E402

# ---------------------------------------------------------------------------
# Valores numericos del enunciado (antes eran enums)
# ---------------------------------------------------------------------------

CORAZON, PULMON, OTRAS = 1, 2, 3
EFECTIVO, TARJETA = 1, 2

# ---------------------------------------------------------------------------
# Fixtures (equivalentes a las de tests/conftest.py)
# ---------------------------------------------------------------------------


@pytest.fixture
def pacienteHabitual() -> Paciente:
    return Paciente("Ana Diaz", CORAZON, True)


@pytest.fixture
def pacienteNoHabitual() -> Paciente:
    return Paciente("Luis Perez", PULMON, False)


@pytest.fixture
def hospitalVacio() -> Hospital:
    return Hospital("Hospital San Roque")


@pytest.fixture
def atencionMedica(pacienteNoHabitual) -> AtencionMedica:
    return AtencionMedica(1, EFECTIVO, pacienteNoHabitual, 1000.0)


@pytest.fixture
def atencionFarmacia() -> AtencionFarmacia:
    return AtencionFarmacia(101, EFECTIVO, 1000.0, 0.0)


def medica(codigo, importe, habitual=False, tipoDeCobro=EFECTIVO):
    """Atencion medica de prueba con un paciente propio."""
    paciente = Paciente(f"Paciente {codigo}", OTRAS, habitual)
    return AtencionMedica(codigo, tipoDeCobro, paciente, importe)


# ---------------------------------------------------------------------------
# Paciente: constructor, acceso, modificacion y toString
# ---------------------------------------------------------------------------


class TestPaciente:

    def test_constructor_registra_los_datos_del_paciente(self):
        paciente = Paciente("Ana Diaz", CORAZON, True)

        assert paciente.nombre == "Ana Diaz"
        assert paciente.sintoma == CORAZON
        assert paciente.habitual is True

    def test_habitual_es_falso_por_defecto(self):
        assert Paciente("Luis Perez", OTRAS).habitual is False

    @pytest.mark.parametrize("sintoma", [CORAZON, PULMON, OTRAS])
    def test_los_sintomas_del_enunciado_son_validos(self, sintoma):
        assert Paciente("Ana Diaz", sintoma).sintoma == sintoma

    @pytest.mark.parametrize("sintoma", [0, 4, "corazon"])
    def test_un_sintoma_fuera_del_enunciado_es_rechazado(self, sintoma):
        with pytest.raises(ValueError):
            Paciente("Ana Diaz", sintoma)

    def test_modificacion_de_los_datos(self, pacienteNoHabitual):
        pacienteNoHabitual.nombre = "Marta Gomez"
        pacienteNoHabitual.sintoma = OTRAS
        pacienteNoHabitual.habitual = True

        assert pacienteNoHabitual.nombre == "Marta Gomez"
        assert pacienteNoHabitual.sintoma == OTRAS
        assert pacienteNoHabitual.habitual is True

    def test_to_string_incluye_los_datos_del_paciente(self, pacienteHabitual):
        cadena = str(pacienteHabitual)

        assert "Ana Diaz" in cadena
        assert "corazon" in cadena


# ---------------------------------------------------------------------------
# AtencionMedica: datos e importeACobrar segun el enunciado
# ---------------------------------------------------------------------------


class TestAtencionMedica:

    def test_constructor_registra_los_datos_de_la_atencion(self, pacienteNoHabitual):
        atencion = AtencionMedica(7, EFECTIVO, pacienteNoHabitual, 1000.0)

        assert atencion.codigo == 7
        assert atencion.tipoDeCobro == EFECTIVO
        assert atencion.paciente is pacienteNoHabitual
        assert atencion.importe == 1000.0

    def test_es_una_atencion(self):
        assert issubclass(AtencionMedica, Atencion)

    def test_atencion_es_abstracta(self):
        with pytest.raises(TypeError):
            Atencion(1, EFECTIVO)

    @pytest.mark.parametrize("tipoDeCobro", [EFECTIVO, TARJETA])
    def test_los_tipos_de_cobro_del_enunciado_son_validos(
        self, tipoDeCobro, pacienteNoHabitual
    ):
        atencion = AtencionMedica(1, tipoDeCobro, pacienteNoHabitual, 1000.0)

        assert atencion.tipoDeCobro == tipoDeCobro

    @pytest.mark.parametrize("tipoDeCobro", [0, 3, "efectivo"])
    def test_un_tipo_de_cobro_fuera_del_enunciado_es_rechazado(
        self, tipoDeCobro, pacienteNoHabitual
    ):
        with pytest.raises(ValueError):
            AtencionMedica(1, tipoDeCobro, pacienteNoHabitual, 1000.0)

    def test_no_habitual_en_efectivo_descuenta_el_10(self, pacienteNoHabitual):
        atencion = AtencionMedica(1, EFECTIVO, pacienteNoHabitual, 1000.0)

        assert atencion.importeACobrar() == pytest.approx(900.0)

    def test_no_habitual_con_tarjeta_recarga_el_20(self, pacienteNoHabitual):
        atencion = AtencionMedica(1, TARJETA, pacienteNoHabitual, 1000.0)

        assert atencion.importeACobrar() == pytest.approx(1200.0)

    def test_habitual_en_efectivo_descuenta_25_y_luego_10(self, pacienteHabitual):
        atencion = AtencionMedica(1, EFECTIVO, pacienteHabitual, 1000.0)

        assert atencion.importeACobrar() == pytest.approx(675.0)

    def test_habitual_con_tarjeta_descuenta_25_y_luego_recarga_20(
        self, pacienteHabitual
    ):
        atencion = AtencionMedica(1, TARJETA, pacienteHabitual, 1000.0)

        assert atencion.importeACobrar() == pytest.approx(900.0)

    def test_es_paciente_habitual(self, pacienteHabitual, pacienteNoHabitual):
        habitual = AtencionMedica(1, EFECTIVO, pacienteHabitual, 1000.0)
        noHabitual = AtencionMedica(2, EFECTIVO, pacienteNoHabitual, 1000.0)

        assert habitual.esPacienteHabitual() is True
        assert noHabitual.esPacienteHabitual() is False

    def test_modificacion_de_los_datos(self, atencionMedica, pacienteHabitual):
        atencionMedica.codigo = 99
        atencionMedica.tipoDeCobro = TARJETA
        atencionMedica.paciente = pacienteHabitual
        atencionMedica.importe = 2000.0

        assert atencionMedica.codigo == 99
        assert atencionMedica.tipoDeCobro == TARJETA
        assert atencionMedica.paciente is pacienteHabitual
        assert atencionMedica.importe == 2000.0

    def test_to_string_incluye_codigo_e_importe_a_cobrar(self, atencionMedica):
        cadena = str(atencionMedica)

        assert "1" in cadena
        assert "900.00" in cadena


# ---------------------------------------------------------------------------
# AtencionFarmacia: datos e importeACobrar segun el enunciado
# ---------------------------------------------------------------------------


class TestAtencionFarmacia:

    def test_constructor_registra_los_datos_de_la_atencion(self):
        atencion = AtencionFarmacia(101, TARJETA, 5000.0, 500.0)

        assert atencion.codigo == 101
        assert atencion.tipoDeCobro == TARJETA
        assert atencion.importeTotal == 5000.0
        assert atencion.descuento == 500.0

    def test_es_una_atencion(self):
        assert issubclass(AtencionFarmacia, Atencion)

    def test_cupon_en_cero_no_aplica_descuento_y_en_efectivo_descuenta_el_5(self):
        atencion = AtencionFarmacia(101, EFECTIVO, 1000.0, 0.0)

        assert atencion.importeACobrar() == pytest.approx(950.0)

    def test_cupon_en_cero_con_tarjeta_recarga_el_30(self):
        atencion = AtencionFarmacia(101, TARJETA, 1000.0, 0.0)

        assert atencion.importeACobrar() == pytest.approx(1300.0)

    def test_el_cupon_se_resta_del_total_y_luego_se_aplica_el_efectivo(self):
        atencion = AtencionFarmacia(101, EFECTIVO, 1000.0, 200.0)

        assert atencion.importeACobrar() == pytest.approx(760.0)

    def test_el_cupon_se_resta_del_total_y_luego_se_aplica_la_tarjeta(self):
        atencion = AtencionFarmacia(101, TARJETA, 1000.0, 200.0)

        assert atencion.importeACobrar() == pytest.approx(1040.0)

    def test_modificacion_de_los_datos(self, atencionFarmacia):
        atencionFarmacia.codigo = 150
        atencionFarmacia.tipoDeCobro = TARJETA
        atencionFarmacia.importeTotal = 3000.0
        atencionFarmacia.descuento = 300.0

        assert atencionFarmacia.codigo == 150
        assert atencionFarmacia.tipoDeCobro == TARJETA
        assert atencionFarmacia.importeTotal == 3000.0
        assert atencionFarmacia.descuento == 300.0

    def test_to_string_incluye_codigo_e_importe_a_cobrar(self, atencionFarmacia):
        cadena = str(atencionFarmacia)

        assert "101" in cadena
        assert "950.00" in cadena


# ---------------------------------------------------------------------------
# Hospital: coleccion de atenciones y metodos del enunciado
# ---------------------------------------------------------------------------


class TestHospital:

    def test_constructor_registra_razon_social_y_coleccion_vacia(self):
        hospital = Hospital("Hospital San Roque")

        assert hospital.razonSocial == "Hospital San Roque"
        assert hospital.atencionesRealizadas == []

    def test_add_atencion_agrega_a_la_coleccion(
        self, hospitalVacio, atencionMedica, atencionFarmacia
    ):
        hospitalVacio.addAtencion(atencionMedica)
        hospitalVacio.addAtencion(atencionFarmacia)

        assert hospitalVacio.atencionesRealizadas == [atencionMedica, atencionFarmacia]

    def test_importe_total_atencion_consulta_suma_los_importes_de_las_consultas(
        self, hospitalVacio
    ):
        hospitalVacio.addAtencion(medica(1, 1000.0))
        hospitalVacio.addAtencion(medica(2, 2500.0, habitual=True))
        hospitalVacio.addAtencion(AtencionFarmacia(101, EFECTIVO, 9999.0, 0.0))

        assert hospitalVacio.importe_total_atencion_consulta() == pytest.approx(3500.0)

    def test_importe_total_atencion_consulta_sin_atenciones_es_cero(
        self, hospitalVacio
    ):
        assert hospitalVacio.importe_total_atencion_consulta() == pytest.approx(0.0)

    def test_importe_promedio_atenciones_solo_promedia_las_del_rango(
        self, hospitalVacio
    ):
        # importeACobrar en efectivo y sin habitual = importe * 0.9 -> 900, 1800 y 2700
        hospitalVacio.addAtencion(medica(1, 1000.0))
        hospitalVacio.addAtencion(medica(2, 2000.0))
        hospitalVacio.addAtencion(medica(3, 3000.0))

        assert hospitalVacio.importe_promedio_atenciones(
            800.0, 2000.0
        ) == pytest.approx(1350.0)

    def test_importe_promedio_atenciones_ignora_las_de_farmacia(self, hospitalVacio):
        hospitalVacio.addAtencion(medica(1, 1000.0))
        hospitalVacio.addAtencion(AtencionFarmacia(101, EFECTIVO, 1000.0, 0.0))

        assert hospitalVacio.importe_promedio_atenciones(0.0, 10000.0) == pytest.approx(
            900.0
        )

    def test_importe_promedio_atenciones_sin_coincidencias_es_cero(self, hospitalVacio):
        hospitalVacio.addAtencion(medica(1, 1000.0))

        assert hospitalVacio.importe_promedio_atenciones(
            5000.0, 9000.0
        ) == pytest.approx(0.0)

    def test_codigo_primera_atencion_habitual_devuelve_la_primera_registrada(
        self, hospitalVacio
    ):
        hospitalVacio.addAtencion(AtencionFarmacia(101, EFECTIVO, 1000.0, 0.0))
        hospitalVacio.addAtencion(medica(2, 1000.0, habitual=False))
        hospitalVacio.addAtencion(medica(3, 1000.0, habitual=True))
        hospitalVacio.addAtencion(medica(4, 1000.0, habitual=True))

        assert hospitalVacio.codigo_primera_atencion_habitual() == 3

    def test_codigo_primera_atencion_habitual_sin_habituales_devuelve_cero(
        self, hospitalVacio
    ):
        hospitalVacio.addAtencion(medica(1, 1000.0, habitual=False))
        hospitalVacio.addAtencion(AtencionFarmacia(101, EFECTIVO, 1000.0, 0.0))

        assert hospitalVacio.codigo_primera_atencion_habitual() == 0

    def test_codigo_primera_atencion_habitual_sin_atenciones_devuelve_cero(
        self, hospitalVacio
    ):
        assert hospitalVacio.codigo_primera_atencion_habitual() == 0

    def test_to_string_incluye_la_razon_social_y_las_atenciones(
        self, hospitalVacio, atencionMedica
    ):
        hospitalVacio.addAtencion(atencionMedica)
        cadena = str(hospitalVacio)

        assert "Hospital San Roque" in cadena
        assert "Atencion Medica 1" in cadena


# ---------------------------------------------------------------------------
# main.py: carga de los archivos CSV de data/
# ---------------------------------------------------------------------------


class TestCargaCsv:

    def test_se_cargan_30_pacientes_indexados_por_codigo_de_atencion(self):
        pacientes = main.cargarPacientes()

        assert len(pacientes) == 30
        assert all(isinstance(codigo, int) for codigo in pacientes)
        assert all(isinstance(paciente, Paciente) for paciente in pacientes.values())

    def test_se_cargan_30_atenciones_medicas_con_su_paciente(self):
        pacientes = main.cargarPacientes()
        medicas = main.cargarAtencionesMedicas(pacientes)

        assert len(medicas) == 30
        assert all(isinstance(atencion, AtencionMedica) for atencion in medicas)
        assert all(
            atencion.paciente is pacientes[atencion.codigo] for atencion in medicas
        )

    def test_se_cargan_30_atenciones_de_farmacia(self):
        farmacia = main.cargarAtencionesFarmacia()

        assert len(farmacia) == 30
        assert all(isinstance(atencion, AtencionFarmacia) for atencion in farmacia)

    def test_el_hospital_queda_cargado_con_las_60_atenciones(self):
        hospital = main.cargarHospital()

        assert len(hospital.atencionesRealizadas) == 60
        assert len(hospital.atencionesMedicas()) == 30

    def test_a_booleano(self):
        assert main.aBooleano("true") is True
        assert main.aBooleano("TRUE") is True
        assert main.aBooleano("false") is False


# ---------------------------------------------------------------------------
# Permite ejecutar el archivo directamente: python test_hospital_autocontenido.py
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v", "-p", "no:cacheprovider"]))
