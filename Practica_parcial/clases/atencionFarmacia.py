from atencion import Atencion

class AtencionFarmacia(Atencion):
    def __init__(self, codigo, tipoDeCobro, importe, descuento):
        super().__init__(codigo, tipoDeCobro)
        self.importe = importe
        self.descuento = descuento

    # --- IMPORTE TOTAL ---
    @property
    def importe(self):
        return self._importe

    @importe.setter
    def importe(self, valor):
        self._importe = float(valor)

    # --- DESCUENTO (CUPÓN) ---
    @property
    def descuento(self):
        return self._descuento

    @descuento.setter
    def descuento(self, valor):
        self._descuento = float(valor)

    def importeACobrar(self):
        monto = self.importe
        monto - self.descuento if self.descuento > 0 else 0 
        if self.tipoDeCobro == 1:
            monto = monto * 0.95
        if self.tipoDeCobro == 2:
            monto = monto * 1.3

            