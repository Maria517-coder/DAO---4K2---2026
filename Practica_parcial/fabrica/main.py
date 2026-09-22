from mantenimientoPreventivo import Preventivo
from mantenimientoCorrectivo import Correctivo
from maquina import Maquina

def principal():
    instancia = Maquina()
    texto = open("mantenimientos.csv")
    for linea in texto:
        dato = linea.split(",")
        tipo = int(dato[0])
        fecha = dato[1]
        operario = dato[2]
        repuestos = float(dato[3])

        if tipo == 1:
            resultado = int(dato[4])
            insumos = int(dato[5])
            mantenimiento = Preventivo(fecha, operario, repuestos, resultado, insumos)

        if tipo == 2:
            horas_parada = int(dato[4])
            tecnico = int(dato[5])
            mantenimiento = Correctivo(fecha, operario, repuestos, horas_parada, tecnico)

        instancia.agregar_mantenimiento(mantenimiento)

    texto.close()

    print(instancia.suma_gastos())
    print(instancia.cantidad_mantenimientos_caros())
    print(instancia.rotura_mas_larga())
    


if __name__ == "__main__":
    principal()