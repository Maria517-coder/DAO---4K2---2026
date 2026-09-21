from sucursal import Sucursal

class Mini(Sucursal):
    def __init__(self, numero, superficie, facturacion, alquiler):
        super().__init__(numero, superficie, facturacion)
        self.alquiler = alquiler

    
    def resultado_comercial(self):
        return self.facturacion - self.alquiler 
    
        
    def es_rentable(self):
        resultadoComercial = self.resultado_comercial()
        indice = resultadoComercial / self.superficie
        if indice > 35:
            return True
        return False
        
        
    def tipo(self):
        return 3

    def indice(self):
        resultadoComercial = self.resultado_comercial()
        indice = resultadoComercial / self.superficie
        return indice
        