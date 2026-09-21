from sucursal import Sucursal

class Super(Sucursal):
    def __init__(self, numero, superficie, facturacion, mayorista):
        super().__init__(numero, superficie, facturacion)
        self.mayorista = mayorista

    
    def resultado_comercial(self):
        return self.facturacion
    
        
    def es_rentable(self):
        resultadoComercial = self.resultado_comercial()
        indice = resultadoComercial / self.superficie
        if self.mayorista and indice > 45:
            return True
        elif not self.mayorista and indice > 40:
            return True
        return False
            
        
    def tipo(self):
        return 2

    def indice(self):
        resultadoComercial = self.resultado_comercial()
        indice = resultadoComercial / self.superficie
        return indice