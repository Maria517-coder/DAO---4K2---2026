from atencion import *
       
class AtencionFarmacia(Atencion):
    def __init__(self, codigo, tipo_de_cobro, importe_total, cupon):
        super().__init__(codigo, tipo_de_cobro)
        self.importe_total = importe_total
        self.cupon = cupon