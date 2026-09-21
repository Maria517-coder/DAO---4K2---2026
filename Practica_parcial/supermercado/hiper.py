from sucursal import Sucursal

class Hiper(Sucursal):
    def __init__(self, numero, superficie, facturacion, alquileres):
        super().__init__(numero, superficie, facturacion)
        self.alquileres = alquileres

    
    def resultado_comercial(self):
        return self.alquileres + self.facturacion
    
        
    def es_rentable(self):
        resultadoComercial = self.resultado_comercial()
        indice = resultadoComercial / self.superficie
        if indice > 50:
            return True
        return False
    
        
    def tipo(self):
        return 1

    def indice(self):
        resultadoComercial = self.resultado_comercial()
        indice = resultadoComercial / self.superficie
        return indice