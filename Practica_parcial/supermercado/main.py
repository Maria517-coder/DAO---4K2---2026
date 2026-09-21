from hiper import Hiper
from mini import Mini
from super import Super
from empresa import Empresa

def main():
    instacia = Empresa()
    texto = open("sucursales.csv")
    for linea in texto:
        dato = linea.split(",")
        tipo  = int(dato[0])
        numero = int(dato[1])
        superficie = int(dato[2])
        facturacion = float(dato[3])

        if tipo == 1:
            alquileres = float(dato[4])
            sucursal = Hiper(numero, superficie, facturacion, alquileres)

        elif tipo == 2:
            mayorista = int(dato[4])
            sucursal = Super(numero, superficie, facturacion, mayorista)

        elif tipo == 3:
            alquiler = float(dato[4])
            sucursal =  Mini(numero, superficie, facturacion, alquiler)

        instacia.agregar_sucursal(sucursal)

    print(instacia.suma_ganancia())
    print(instacia.cantidad_no_rentables())
    print(instacia.local_mas_rentable())


if __name__ == "__main__":
    main()
